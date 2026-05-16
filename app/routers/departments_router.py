from fastapi import APIRouter, Depends, Query, status

from app.dependencies.departments_dependencies import get_departments_service
from app.schemas.department import (
    DepartmentCreate,
    DepartmentRead,
    DepartmentTreeRead,
    DepartmentUpdate,
)
from app.schemas.employee import EmployeeCreate, EmployeeRead
from app.services.department_service import DepartmentService

router = APIRouter(prefix="/departments", tags=["departments"])


@router.post(
    "/",
    response_model=DepartmentRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_department(
    data: DepartmentCreate,
    departments_service: DepartmentService = Depends(get_departments_service),
):
    return await departments_service.create_department(data)


@router.get(
    "/{department_id}",
    response_model=DepartmentTreeRead,
)
async def get_department(
    department_id: int,
    depth: int = Query(default=1, ge=0, le=5),
    include_employees: bool = True,
    departments_service: DepartmentService = Depends(get_departments_service),
):
    return await departments_service.get_department_tree(
        department_id=department_id,
        depth=depth,
        include_employees=include_employees,
    )


@router.post(
    "/{department_id}/employees/",
    response_model=EmployeeRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_employee_for_department(
    department_id: int,
    data: EmployeeCreate,
    departments_service: DepartmentService = Depends(get_departments_service),
):
    return await departments_service.create_employee_for_department(
        department_id=department_id,
        data=data,
    )


@router.patch(
    "/{department_id}",
    response_model=DepartmentRead,
)
async def update_department(
    department_id: int,
    data: DepartmentUpdate,
    departments_service: DepartmentService = Depends(get_departments_service),
):
    return await departments_service.update_department(
        department_id=department_id,
        data=data,
    )


@router.delete(
    "/{department_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_department(
    department_id: int,
    mode: str = Query(..., pattern="^(cascade|reassign)$"),
    reassign_to_department_id: int | None = None,
    departments_service: DepartmentService = Depends(get_departments_service),
):
    await departments_service.delete_department(
        department_id=department_id,
        mode=mode,
        reassign_to_department_id=reassign_to_department_id,
    )
