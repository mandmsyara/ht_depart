from fastapi import HTTPException, status


class DepartmentAlreadyExistError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail="Department already exists",
        )


class DepartmentNotFoundError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found",
        )


class ParentDepartmentNotFoundError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Parent department not found",
        )


class DepartmentCannotBeParentOfItselfError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail="Department cannot be parent of itself",
        )


class DepartmentCycleError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cannot move department into its own subtree",
        )


class ReassignDepartmentRequiredError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="reassign_to_department_id is required for reassign mode",
        )


class InvalidDeleteModeError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Delete mode must be 'cascade' or 'reassign'",
        )


class CannotReassignToSameDepartmentError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cannot reassign employees to the same department",
        )
