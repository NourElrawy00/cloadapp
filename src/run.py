from app import CreateApp
import sys

app = CreateApp()

if __name__ == '__main__':
    # Development only - NEVER use app.run() in production
    print("WARNING: Running development server. Use a WSGI server for production.", file=sys.stderr)
    app.run(debug=False, host='127.0.0.1', port=8000)