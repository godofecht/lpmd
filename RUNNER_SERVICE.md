# LPMD Runner Service

This service provides backend execution for the LPMD GitHub Pages site, allowing actual Python interpreter execution instead of client-side simulation.

## Deployment Options

### Option 1: Docker Deployment

1. Build and run the service with Docker:

```bash
docker build -t lpmd-runner .
docker run -p 5000:5000 lpmd-runner
```

Or use docker-compose:

```bash
docker-compose up -d
```

### Option 2: Direct Python Execution

1. Install dependencies:

```bash
pip install flask
pip install -r requirements.txt
```

2. Run the service:

```bash
cd src/web
python lpmd_runner.py
```

## API Endpoint

The service provides a single endpoint:

- POST `/execute` - Execute LPMD code using the actual Python interpreter

Request body:
```json
{
  "code": "Your LPMD code here..."
}
```

Response:
```json
{
  "success": true/false,
  "output": "Execution output",
  "returncode": 0
}
```

## Updating the Frontend

To use the actual backend service instead of the simulation:

1. Update the `runLPMD()` function in `index.html` to call your deployed service:

```javascript
async function runLPMD() {
    const input = document.getElementById('lpmd-input').value;
    const output = document.getElementById('lpmd-output');
    
    output.value = 'Executing with the actual LPMD system...\n';
    
    try {
        const response = await fetch('https://your-deployed-service.com/execute', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ code: input })
        });
        
        const result = await response.json();
        
        output.value = result.output;
        
        if (!result.success) {
            output.value += `\nExecution failed with return code: ${result.returncode}`;
        }
    } catch (error) {
        output.value = `Error: ${error.message}`;
    }
}
```

## Deployment Platforms

You can deploy this service to various platforms:

- **Heroku**: Use the provided Procfile (create one if needed)
- **Railway**: Connect your GitHub repo directly
- **Google Cloud Run**: Containerized deployment
- **AWS Elastic Beanstalk**: Platform-as-a-Service
- **Self-hosted**: Run on any server with Python support

## Security Considerations

⚠️ **Important**: This service executes arbitrary Python code. Only deploy in secure environments with appropriate sandboxing if accepting code from untrusted sources.