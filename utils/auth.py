# FILE: utils/auth.py

from fastapi import Request, HTTPException, status
from utils.supabase import supabase

async def verify(request: Request):
    """
    Verify the requester is a valid student or teacher.
    Works with both cookies and headers.
    Returns both user_id and role for downstream use.
    """
    user_id = request.cookies.get("user_id") or request.headers.get("user_id")
    role = request.cookies.get("role") or request.headers.get("role")

    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing user_id")

    if role not in ["student", "teacher"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid role")

    # Check if user exists in the correct table
    table = "students" if role == "student" else "teachers"
    res = supabase.table(table).select("id").eq("id", user_id).execute()

    if not res.data:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User not found in database")

    # Return both user_id and role
    return {"user_id": user_id, "role": role}