import {
	IExecuteFunctions,
	INodeExecutionData,
	INodeType,
	INodeTypeDescription,
	NodeOperationError,
} from 'n8n-workflow';

export class StoryMemorySearch implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'Story Memory Search',
		name: 'storyMemorySearch',
		icon: 'fa:book-open',
		group: ['input'],
		version: 1,
		subtitle: '={{$parameter["operation"]}}',
		description: 'Search and retrieve stories from Story Memory API for context in other prompts',
		defaults: {
			name: 'Story Memory Search',
		},
		inputs: ['main'],
		outputs: ['main'],
		credentials: [
			{
				name: 'storyMemoryApi',
				required: true,
			},
		],
		properties: [
			{
				displayName: 'Operation',
				name: 'operation',
				type: 'options',
				noDataExpression: true,
				options: [
					{
						name: 'Search Stories',
						value: 'searchStories',
						description: 'Search stories by keywords or semantic similarity',
						action: 'Search stories by keywords or semantic similarity',
					},
					{
						name: 'Get Child Stories',
						value: 'getChildStories', 
						description: 'Get all stories for a specific child',
						action: 'Get all stories for a child',
					},
					{
						name: 'Get Child Profile',
						value: 'getChildProfile',
						description: 'Get child profile information',
						action: 'Get child profile information',
					},
					{
						name: 'Get Latest Story',
						value: 'getLatestStory',
						description: 'Get the most recent story for a child',
						action: 'Get the most recent story for a child',
					},
				],
				default: 'searchStories',
			},
			{
				displayName: 'Child ID',
				name: 'childId',
				type: 'number',
				required: true,
				default: 1,
				description: 'The ID of the child',
			},
			{
				displayName: 'Search Query',
				name: 'query',
				type: 'string',
				displayOptions: {
					show: {
						operation: ['searchStories'],
					},
				},
				default: '',
				description: 'Search term for finding relevant stories',
				placeholder: 'adventure, friendship, dragons...',
			},
			{
				displayName: 'Limit',
				name: 'limit',
				type: 'number',
				displayOptions: {
					show: {
						operation: ['searchStories', 'getChildStories'],
					},
				},
				default: 5,
				description: 'Maximum number of stories to return',
				typeOptions: {
					minValue: 1,
					maxValue: 50,
				},
			},
			{
				displayName: 'Output Format',
				name: 'outputFormat',
				type: 'options',
				options: [
					{
						name: 'Full Story Objects',
						value: 'full',
						description: 'Return complete story data including embeddings',
					},
					{
						name: 'Text Only',
						value: 'text',
						description: 'Return only story text for use as context',
					},
					{
						name: 'Summary',
						value: 'summary',
						description: 'Return story summaries and keywords',
					},
				],
				default: 'text',
				description: 'How to format the output for downstream nodes',
			},
		],
	};

	async execute(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
		const items = this.getInputData();
		const returnData: INodeExecutionData[] = [];
		const credentials = await this.getCredentials('storyMemoryApi');

		const baseUrl = credentials.baseUrl as string || 'https://jackskehan.tech/storyAPI';
		const apiKey = credentials.apiKey as string;

		const headers = {
			'Authorization': `Bearer ${apiKey}`,
			'Content-Type': 'application/json',
		};

		for (let i = 0; i < items.length; i++) {
			const operation = this.getNodeParameter('operation', i) as string;
			const childId = this.getNodeParameter('childId', i) as number;
			const outputFormat = this.getNodeParameter('outputFormat', i) as string;

			try {
				let responseData;
				let url: string;

				switch (operation) {
					case 'searchStories':
						const query = this.getNodeParameter('query', i) as string;
						const searchLimit = this.getNodeParameter('limit', i) as number;
						
						url = `${baseUrl}/stories/search?child_id=${childId}&limit=${searchLimit}`;
						if (query) {
							url += `&query=${encodeURIComponent(query)}`;
						}
						
						responseData = await this.helpers.request({
							method: 'GET',
							url,
							headers,
							json: true,
						});
						break;

					case 'getChildStories':
						const storiesLimit = this.getNodeParameter('limit', i) as number;
						url = `${baseUrl}/stories/${childId}?limit=${storiesLimit}`;
						
						responseData = await this.helpers.request({
							method: 'GET',
							url,
							headers,
							json: true,
						});
						break;

					case 'getChildProfile':
						url = `${baseUrl}/children/${childId}`;
						
						responseData = await this.helpers.request({
							method: 'GET',
							url,
							headers,
							json: true,
						});
						break;

					case 'getLatestStory':
						url = `${baseUrl}/stories/latest/${childId}`;
						
						responseData = await this.helpers.request({
							method: 'GET',
							url,
							headers,
							json: true,
						});
						break;

					default:
						throw new NodeOperationError(this.getNode(), `Unknown operation: ${operation}`);
				}

				// Format output based on user preference
				if (Array.isArray(responseData) && outputFormat !== 'full') {
					responseData = responseData.map(story => {
						switch (outputFormat) {
							case 'text':
								return {
									story_text: story.story_text,
									summary: story.summary,
									keywords: story.keywords,
									id: story.id,
								};
							case 'summary':
								return {
									id: story.id,
									summary: story.summary,
									keywords: story.keywords,
									difficulty: story.difficulty,
									created_at: story.created_at,
								};
							default:
								return story;
						}
					});
				} else if (!Array.isArray(responseData) && outputFormat === 'text' && responseData.story_text) {
					// Single story object
					responseData = {
						story_text: responseData.story_text,
						summary: responseData.summary,
						keywords: responseData.keywords,
						id: responseData.id,
					};
				}

				returnData.push({
					json: {
						operation,
						childId,
						data: responseData,
						// Add metadata for context usage
						contextSummary: Array.isArray(responseData) 
							? `Found ${responseData.length} stories for child ${childId}`
							: `Retrieved data for child ${childId}`,
					},
				});

			} catch (error) {
				if (this.continueOnFail()) {
					returnData.push({
						json: {
							error: error.message,
							operation,
							childId,
						},
						error,
					});
				} else {
					throw new NodeOperationError(this.getNode(), error.message);
				}
			}
		}

		return [returnData];
	}
}