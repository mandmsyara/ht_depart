from app.exception.exception import (
    CannotReassignToSameDepartmentError,
    DepartmentAlreadyExistError,
    DepartmentCannotBeParentOfItselfError,
    DepartmentCycleError,
    DepartmentNotFoundError,
    InvalidDeleteModeError,
    ParentDepartmentNotFoundError,
    ReassignDepartmentRequiredError,
)
from app.models.department import Department
from app.models.employee import Employee
from app.repositories.department_repository import DepartmentRepository
from app.repositories.employee_repository import EmployeeRepository
from app.schemas.department import (
    DepartmentCreate,
    DepartmentTreeRead,
    DepartmentUpdate,
)
from app.schemas.employee import EmployeeCreate, EmployeeRead


class DepartmentService:
    def __init__(
        self, department_repo: DepartmentRepository, employee_repo: EmployeeRepository
    ):
        self.department_repo = department_repo
        self.employee_repo = employee_repo

    async def create_department(
        self,
        data: DepartmentCreate,
    ):
        if data.parent_id is not None:
            parent_department = await self.department_repo.get_department_by_id(
                data.parent_id,
            )

            if parent_department is None:
                raise ParentDepartmentNotFoundError()

        existing_department = (
            await self.department_repo.get_department_by_name_and_parent(
                data.name,
                data.parent_id,
            )
        )

        if existing_department is not None:
            raise DepartmentAlreadyExistError()

        department = await self.department_repo.create_department(
            department_name=data.name,
            parent_id=data.parent_id,
        )

        return department

    async def get_department_tree(
        self,
        department_id: int,
        depth: int = 1,
        include_employees: bool = True,
    ) -> DepartmentTreeRead:
        department = await self.department_repo.get_department_with_relations(
            department_id
        )

        if department is None:
            raise DepartmentNotFoundError()

        return self._build_department_tree(
            department=department,
            depth=depth,
            include_employees=include_employees,
        )

    def _build_department_tree(
        self,
        department: Department,
        depth: int,
        include_employees: bool,
    ) -> DepartmentTreeRead:
        employees = []

        if include_employees:
            employees = [
                EmployeeRead.model_validate(employee)
                for employee in sorted(
                    department.employees,
                    key=lambda employee: employee.full_name,
                )
            ]

        children = []

        if depth > 0:
            children = [
                self._build_department_tree(
                    department=child,
                    depth=depth - 1,
                    include_employees=include_employees,
                )
                for child in department.children
            ]

        return DepartmentTreeRead(
            id=department.id,
            name=department.name,
            parent_id=department.parent_id,
            created_at=department.created_at,
            employees=employees,
            children=children,
        )

    async def create_employee_for_department(
        self,
        department_id: int,
        data: EmployeeCreate,
    ) -> Employee:
        department = await self.department_repo.get_department_by_id(department_id)

        if department is None:
            raise DepartmentNotFoundError()

        return await self.employee_repo.create_employee(
            department_id=department_id,
            full_name=data.full_name,
            position=data.position,
            hired_at=data.hired_at,
        )

    async def _is_descendant(
        self,
        department_id: int,
        potential_parent_id: int,
    ) -> bool:
        children = await self.department_repo.get_children(department_id)

        for child in children:
            if child.id == potential_parent_id:
                return True

            is_nested = await self._is_descendant(
                department_id=child.id,
                potential_parent_id=potential_parent_id,
            )

            if is_nested:
                return True

        return False

    async def update_department(
        self,
        department_id: int,
        data: DepartmentUpdate,
    ) -> Department:
        department = await self.department_repo.get_department_by_id(department_id)

        if department is None:
            raise DepartmentNotFoundError()

        if "parent_id" in data.model_fields_set:
            if data.parent_id == department.id:
                raise DepartmentCannotBeParentOfItselfError()

            if data.parent_id is not None:
                new_parent = await self.department_repo.get_department_by_id(
                    data.parent_id
                )

                if new_parent is None:
                    raise ParentDepartmentNotFoundError()

                is_descendant = await self._is_descendant(
                    department_id=department.id,
                    potential_parent_id=data.parent_id,
                )

                if is_descendant:
                    raise DepartmentCycleError()

        target_parent_id = (
            data.parent_id
            if "parent_id" in data.model_fields_set
            else department.parent_id
        )

        target_name = data.name if data.name is not None else department.name

        existing_department = (
            await self.department_repo.get_department_by_name_and_parent(
                department_name=target_name,
                parent_id=target_parent_id,
            )
        )

        if existing_department is not None and existing_department.id != department.id:
            raise DepartmentAlreadyExistError()

        return await self.department_repo.update_department(
            department=department,
            new_name=data.name,
            parent_id_was_provided="parent_id" in data.model_fields_set,
            new_parent_id=data.parent_id,
        )

    async def delete_department(
        self,
        department_id: int,
        mode: str,
        reassign_to_department_id: int | None = None,
    ) -> None:
        department = await self.department_repo.get_department_by_id(department_id)

        if department is None:
            raise DepartmentNotFoundError()

        if mode not in ("cascade", "reassign"):
            raise InvalidDeleteModeError()

        if mode == "cascade":
            await self.department_repo.delete_department(department)
            return

        if reassign_to_department_id is None:
            raise ReassignDepartmentRequiredError()

        if reassign_to_department_id == department_id:
            raise CannotReassignToSameDepartmentError()

        target_department = await self.department_repo.get_department_by_id(
            reassign_to_department_id
        )

        if target_department is None:
            raise DepartmentNotFoundError()

        await self.employee_repo.reassign_department(
            old_department_id=department_id,
            new_department_id=reassign_to_department_id,
        )

        await self.department_repo.delete_department(department)
