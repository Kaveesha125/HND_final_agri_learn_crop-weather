from fastapi import Request, HTTPException, status
from utils.supabase import supabase

async def verify(request: Request):

    token = None
    user_id_from_header = None
    role_from_header = None


    gateway_user_id = request.headers.get("X-User-Id")
    gateway_role = request.headers.get("X-User-Role")

    if gateway_user_id and gateway_role:
        print("DEBUG: Using Gateway Headers for Auth")
        user_id_from_header = gateway_user_id
        role_from_header = gateway_role
        if role_from_header not in ["student", "teacher", "admin"]: # Include admin if applicable
             raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid role from Gateway: {role_from_header}")
        return {"user_id": user_id_from_header, "role": role_from_header}

    token = request.cookies.get("access_token")
    print(f"DEBUG: Token from cookie: {'Present' if token else 'Missing'}") # Add more logging

    if not token:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
             print("DEBUG: Falling back to Authorization header")
             token = auth_header.split(" ")[1]

    if not token:
        print("DEBUG: No token found in cookies or headers.")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing access token (cookie or header)")

    try:
        print("DEBUG: Attempting Supabase token validation...")
        user_response = supabase.auth.get_user(token)

        if not user_response or not user_response.user:
            print("DEBUG: Supabase validation failed: No user returned.")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token (Supabase)")

        user = user_response.user
        user_id = user.id
        role = user.user_metadata.get("role", "student") if user.user_metadata else "student"
        print(f"DEBUG: Supabase validation successful. UserID: {user_id}, Role: {role}")

        if role not in ["student", "teacher", "admin"]: # Ensure role is valid
            print(f"DEBUG: Invalid role '{role}' found in token metadata.")
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid role found in token: {role}")

        print(f"DEBUG: User verified successfully. UserID: {user_id}, Role: {role}")
        return {"user_id": user_id, "role": role}

    except HTTPException as e:
         print(f"DEBUG: HTTPException during verification: {e.detail}")
         raise e
    except Exception as e:
        print(f"DEBUG: Unexpected error during Supabase validation: {str(e)}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Token validation failed: {str(e)}")