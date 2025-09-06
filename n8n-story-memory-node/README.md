# n8n-nodes-story-memory

This package provides n8n nodes to integrate with the Story Memory API, allowing you to search and retrieve story context for use in AI prompts and workflows.

![n8n.io - Workflow Automation](https://raw.githubusercontent.com/n8n-io/n8n/master/assets/n8n-logo.png)

## Features

- **Search Stories**: Find relevant stories by keywords or semantic similarity
- **Get Child Stories**: Retrieve all stories for a specific child
- **Get Child Profile**: Access child information and preferences
- **Get Latest Story**: Fetch the most recent story for a child
- **Flexible Output**: Choose between full data, text-only, or summary formats

## Installation

### Community Nodes (Recommended)

1. In n8n, go to **Settings** → **Community Nodes**
2. Click **Install a Community Node**
3. Enter: `n8n-nodes-story-memory`
4. Click **Install**

### Manual Installation

1. Navigate to your n8n installation directory
2. Run: `npm install n8n-nodes-story-memory`
3. Restart n8n

## Configuration

### 1. Set up Credentials

1. In n8n, go to **Credentials** → **Create New**
2. Search for **Story Memory API**
3. Enter your credentials:
   - **API Key**: Your Story Memory API bearer token
   - **Base URL**: `https://jackskehan.tech/storyAPI` (or your custom URL)
4. Click **Test** to verify connection
5. Save the credential

### 2. Use the Node

1. Add **Story Memory Search** node to your workflow
2. Select your credential
3. Configure the operation:
   - **Search Stories**: Find stories by query terms
   - **Get Child Stories**: Get all stories for a child
   - **Get Child Profile**: Get child information
   - **Get Latest Story**: Get most recent story

## Node Parameters

### Common Parameters
- **Child ID** (required): The ID of the child
- **Output Format**: Choose how data is returned:
  - **Text Only**: Just story text and summary (best for AI context)
  - **Summary**: Story metadata and keywords
  - **Full Story Objects**: Complete story data including embeddings

### Search Stories Parameters
- **Search Query**: Keywords or phrases to search for
- **Limit**: Maximum number of stories to return (1-50, default: 5)

### Get Child Stories Parameters
- **Limit**: Maximum number of stories to return (1-50, default: 5)

## Usage Examples

### Example 1: Context for AI Chat
```
Story Memory Search (Search Stories) 
→ Set Node (format for prompt)
→ OpenAI Chat
```

**Configuration**:
- Operation: Search Stories
- Child ID: 1
- Search Query: "friendship adventure"
- Output Format: Text Only
- Limit: 3

### Example 2: Get Latest Story for Continuation
```
Story Memory Search (Get Latest Story)
→ OpenAI Chat (continue the story)
→ HTTP Request (save new story)
```

### Example 3: Workflow with Context
```
Webhook (trigger)
→ Story Memory Search (get relevant stories)
→ Set Node (combine with user input)
→ OpenAI Chat (generate response with context)
→ Respond to Webhook
```

## Output Format Examples

### Text Only Output
```json
{
  "operation": "searchStories",
  "childId": 1,
  "data": [
    {
      "id": 15,
      "story_text": "Once upon a time, there was a brave dragon...",
      "summary": "A story about friendship and courage",
      "keywords": ["dragon", "friendship", "adventure"]
    }
  ],
  "contextSummary": "Found 3 stories for child 1"
}
```

### Summary Output
```json
{
  "operation": "searchStories", 
  "childId": 1,
  "data": [
    {
      "id": 15,
      "summary": "A story about friendship and courage",
      "keywords": ["dragon", "friendship", "adventure"],
      "difficulty": 2,
      "created_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

## API Operations

- **GET /stories/search**: Search stories by keywords or semantic similarity
- **GET /stories/{child_id}**: Get all stories for a child
- **GET /children/{child_id}**: Get child profile information  
- **GET /stories/latest/{child_id}**: Get most recent story for a child

## Error Handling

The node includes built-in error handling:
- **401 Unauthorized**: Invalid API key
- **400 Bad Request**: Invalid parameters
- **404 Not Found**: Child or story not found
- **422 Unprocessable Entity**: Validation errors

Enable **Continue on Fail** to handle errors gracefully in your workflow.

## Development

### Building the Node
```bash
npm install
npm run build
```

### Development Mode
```bash
npm run dev
```

### Testing
Link the package to your n8n installation for testing:
```bash
# In this package directory
npm link

# In your n8n installation directory  
npm link n8n-nodes-story-memory
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT

## Support

- [Story Memory API Documentation](https://jackskehan.tech/storyAPI)
- [n8n Community Forum](https://community.n8n.io)
- [GitHub Issues](https://github.com/yourusername/n8n-nodes-story-memory/issues)

## Version History

- **1.0.0**: Initial release with search, get stories, get profile, and get latest story operations