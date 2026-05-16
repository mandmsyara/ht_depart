from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.department import Department


class DepartmentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_department_by_id(
        self,
        department_id: int,
    ) -> Department | None:
        stmt = select(Department).where(Department.id == department_id)

        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()

    async def get_department_by_name_and_parent(
        self,
        department_name: str,
        parent_id: int | None = None,
    ) -> Department | None:
        stmt = select(Department).where(
            Department.name == department_name,
            Department.parent_id == parent_id,
        )

        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()

    async def create_department(
        self,
        department_name: str,
        parent_id: int | None = None,
    ) -> Department:
        department = Department(name=department_name, parent_id=parent_id)

        self.session.add(department)

        await self.session.commit()
        await self.session.refresh(department)

        return department

    async def delete_department(
        self,
        department: Department,
    ) -> None:
        await self.session.delete(department)
        await self.session.commit()

    async def update_department(
        self,
        department: Department,
        *,
        new_name: str | None = None,
        parent_id_was_provided: bool = False,
        new_parent_id: int | None = None,
    ) -> Department:
        if new_name is not None:
            department.name = new_name

        if parent_id_was_provided:
            department.parent_id = new_parent_id

        await self.session.commit()
        await self.session.refresh(department)

        return department

    async def get_department_with_relations(
        self,
        department_id: int,
    ) -> Department | None:
        stmt = (
            select(Department)
            .where(Department.id == department_id)
            .options(
                selectinload(Department.employees),
                selectinload(Department.children).selectinload(Department.employees),
                selectinload(Department.children).selectinload(Department.children),
            )
        )

        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()

    async def get_children(
        self,
        department_id: int,
    ) -> list[Department]:
        stmt = select(Department).where(Department.parent_id == department_id)

        result = await self.session.execute(stmt)

        return list(result.scalars().all())
