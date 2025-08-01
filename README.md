# LLM-Powered Intelligent Query-Retrieval System with Google Gemini

A sophisticated document processing and query system designed for **insurance, legal, HR, and compliance domains** using **Google Gemini API**.

## 🚀 Features

- **Multi-format Document Processing**: PDF, DOCX parsing from blob URLs
- **Semantic Search**: FAISS-powered vector similarity search  
- **Google Gemini Integration**: Advanced LLM responses using Gemini 2.0 Flash
- **Insurance Domain Optimized**: Specialized for policy and compliance documents
- **RESTful API**: Easy integration with `/hackrx/run` endpoint
- **Real-time Processing**: Efficient handling of large documents

## 🏗 System Architecture

```
1. Input Documents (PDF Blob URL) 
   ↓
2. Document Parser (PDF/DOCX extraction)
   ↓  
3. Embedding Search (FAISS vector similarity)
   ↓
4. Clause Matching (Semantic similarity)
   ↓
5. Gemini Processing (Query understanding + Answer generation)
   ↓
6. JSON Output (Structured response)
```

## 📋 Requirements

- Python 3.9+
- Google Gemini API Key
- 2GB+ RAM (for embedding models)
- Internet connection for document downloads

## 🛠 Installation & Setup

### 1. Get Gemini API Key
1. Go to [Google AI Studio](https://aistudio.google.com)
2. Sign in with your Google account
3. Create an API key
4. Copy the API key for later use

### 2. Local Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Set your Gemini API key in .env file
GEMINI_API_KEY=your_actual_gemini_api_key_here
```

### 3. Run Locally
```bash
python main.py
```

The server will start on `http://localhost:8000`

## 🚀 Deploy on Render.com

### Step 1: Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/your-username/your-repo.git
git push -u origin main
```

### Step 2: Deploy on Render
1. Go to [render.com](https://render.com) and sign up
2. Click "New" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python main.py`
   - **Environment Variables**:
     - `GEMINI_API_KEY`: your_actual_gemini_api_key
     - `PORT`: 8000

### Step 3: Test Your Deployed API
Your API will be available at: `https://your-app-name.onrender.com`

## 📚 API Usage

### Authentication
All requests require the Bearer token:
```
Authorization: Bearer c0df38f44acb385ecd42f8e0c02ee14acd6d145835643ee57acd84f79afeb798
```

### Main Endpoint: POST /hackrx/run

**Request:**
```json
{
    "documents": "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D",
    "questions": [
        "What is the grace period for premium payment under the National Parivar Mediclaim Plus Policy?",
        "What is the waiting period for pre-existing diseases (PED) to be covered?",
        "Does this policy cover maternity expenses, and what are the conditions?"
    ]
}
```

**Response:**
```json
{
    "answers": [
        "A grace period of thirty days is provided for premium payment after the due date to renew or continue the policy without losing continuity benefits.",
        "There is a waiting period of thirty-six (36) months of continuous coverage from the first policy inception for pre-existing diseases and their direct complications to be covered.",
        "Yes, the policy covers maternity expenses, including childbirth and lawful medical termination of pregnancy. To be eligible, the female insured person must have been continuously covered for at least 24 months."
    ]
}
```

### Example cURL Request
```bash
curl -X POST "https://your-app.onrender.com/hackrx/run" \
  -H "Authorization: Bearer c0df38f44acb385ecd42f8e0c02ee14acd6d145835643ee57acd84f79afeb798" \
  -H "Content-Type: application/json" \
  -d '{
    "documents": "https://example.com/policy.pdf",
    "questions": ["What is the grace period for premium payment?"]
  }'
```

### Other Endpoints

- **GET /** - Health check
- **GET /health** - Detailed system health  
- **GET /status** - API status and version

## 🔧 Configuration

### Environment Variables
| Variable | Description | Default |
|----------|-------------|---------|
| `GEMINI_API_KEY` | Google Gemini API key | Required |
| `BEARER_TOKEN` | API authentication token | Set |
| `PORT` | Server port | 8000 |
| `CHUNK_SIZE` | Document chunk size | 1000 |
| `MAX_CONTEXT_CHUNKS` | Max chunks per query | 3 |

## 🎯 Domain-Specific Features

### Insurance Policies
- Premium payment terms
- Coverage definitions  
- Exclusion identification
- Waiting period extraction
- Claim procedures

### Legal Contracts
- Clause analysis
- Terms and conditions
- Liability assessment
- Compliance requirements

### HR Documents  
- Policy interpretation
- Benefit explanations
- Procedure guidelines

## 🧪 Testing

### Health Check
```bash
curl https://your-app.onrender.com/health
```

### API Status  
```bash
curl https://your-app.onrender.com/status
```

## 🔍 Troubleshooting

### Common Issues

1. **Gemini API Errors**
   - Verify API key in `.env` file
   - Check API quotas and limits
   - Ensure Gemini API is enabled

2. **Document Processing Errors**
   - Verify document URL is accessible
   - Check supported formats (PDF, DOCX)
   - Review file size limitations

3. **Memory Issues**
   - Reduce `CHUNK_SIZE`
   - Lower `MAX_CONTEXT_CHUNKS`

### Getting Your Gemini API Key
1. Visit [Google AI Studio](https://aistudio.google.com)
2. Sign in with Google account
3. Click "Get API Key"
4. Create new API key
5. Copy and use in your `.env` file

## 🛡 Security

- Bearer token authentication
- Input validation and sanitization  
- Secure credential management
- Rate limiting support

## 📊 Performance

- **Document Processing**: ~2-5 seconds for typical PDFs
- **Query Response**: ~1-3 seconds per question
- **Concurrent Requests**: Supports multiple simultaneous requests
- **Memory Usage**: ~500MB-1GB depending on document size

## 🏆 HackRx Implementation

This system addresses all HackRx requirements:

✅ **1. Input Documents**: PDF Blob URL processing  
✅ **2. LLM Parser**: Gemini-powered query extraction  
✅ **3. Embedding Search**: FAISS vector retrieval  
✅ **4. Clause Matching**: Semantic similarity matching  
✅ **5. Logic Evaluation**: Context-aware decision processing  
✅ **6. JSON Output**: Structured response format  

## 🤝 Support

For deployment and API issues:
- Check the troubleshooting section
- Review Render deployment logs
- Verify environment variables are set correctly

---

**Built for HackRx 2025 with Google Gemini** 🚀
