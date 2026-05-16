from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.employee import Employee


class EmployeeRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_employee(
        self,
        department_id: int,
        full_name: str,
        position: str,
        hired_at,
    ) -> Employee:
        employee = Employee(
            department_id=department_id,
            full_name=full_name,
            position=position,
            hired_at=hired_at,
        )

        self.session.add(employee)

        await self.session.commit()
        await self.session.refresh(employee)

        return employee

    async def reassign_department(
        self,
        old_department_id: int,
        new_department_id: int,
    ) -> None:
        stmt = (
            update(Employee)
            .where(Employee.department_id == old_department_id)
            .values(department_id=new_department_id)
        )

        await self.session.execute(stmt)
        await self.session.commit()
