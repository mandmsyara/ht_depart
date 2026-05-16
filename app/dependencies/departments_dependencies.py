from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_async_session
from app.repositories.department_repository import DepartmentRepository
from app.repositories.employee_repository import EmployeeRepository
from app.services.department_service import DepartmentService


def get_departments_repository(
    session: AsyncSession = Depends(get_async_session),
) -> DepartmentRepository:
    return DepartmentRepository(session)


def get_employee_repository(
    session: AsyncSession = Depends(get_async_session),
) -> EmployeeRepository:
    return EmployeeRepository(session)


def get_departments_service(
    department_repo: DepartmentRepository = Depends(get_departments_repository),
    employee_repo: EmployeeRepository = Depends(get_employee_repository),
) -> DepartmentService:
    return DepartmentService(
        department_repo=department_repo,
        employee_repo=employee_repo,
    )
