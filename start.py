import os
import uvicorn
import sys

if __name__ == "__main__":
    # Debug logging for environment variables
    print("Environment variables:")
    print(f"Raw PORT value: {os.environ.get('PORT', 'not set')}")
    print(f"All env vars: {dict(os.environ)}")
    
    try:
        # Get port from environment variable with a default fallback
        port = int(os.getenv("PORT", "8000"))
        print(f"Parsed port value: {port}")
        
        # Run the FastAPI application
        print(f"Starting uvicorn with port: {port}")
        sys.stdout.flush()  # Force flush the output
        
        uvicorn.run(
            "app.main:app",
            host="0.0.0.0",
            port=port,
            proxy_headers=True,
            forwarded_allow_ips="*"
        )
    except ValueError as e:
        print(f"Error parsing PORT value: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1) 