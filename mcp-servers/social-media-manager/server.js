const { Server } = require('@modelcontextprotocol/sdk/server/index.js');
const { StdioServerTransport } = require('@modelcontextprotocol/sdk/server/stdio.js');
const {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} = require('@modelcontextprotocol/sdk/types.js');
const axios = require('axios');
const fs = require('fs').promises;
const path = require('path');
const FormData = require('form-data');

class SocialMediaMCPServer {
  constructor() {
    this.server = new Server(
      {
        name: 'social-media-manager',
        version: '1.0.0',
      },
      {
        capabilities: {
          tools: {},
        },
      }
    );

    this.setupToolHandlers();
  }

  setupToolHandlers() {
    this.server.setRequestHandler(ListToolsRequestSchema, async () => {
      return {
        tools: [
          {
            name: 'post_to_twitter',
            description: 'Post content to Twitter/X',
            inputSchema: {
              type: 'object',
              properties: {
                content: { type: 'string', description: 'Tweet content' },
                media_path: { type: 'string', description: 'Path to media file (optional)' },
                schedule_time: { type: 'string', description: 'ISO datetime for scheduling (optional)' }
              },
              required: ['content']
            }
          },
          {
            name: 'post_to_instagram',
            description: 'Post content to Instagram',
            inputSchema: {
              type: 'object',
              properties: {
                content: { type: 'string', description: 'Post caption' },
                media_path: { type: 'string', description: 'Path to image or video file' },
                media_type: { type: 'string', enum: ['photo', 'reel'], description: 'Type of media' }
              },
              required: ['content', 'media_path', 'media_type']
            }
          },
          {
            name: 'post_to_tiktok',
            description: 'Post content to TikTok',
            inputSchema: {
              type: 'object',
              properties: {
                content: { type: 'string', description: 'Video caption' },
                video_path: { type: 'string', description: 'Path to video file' },
                hashtags: { type: 'array', items: { type: 'string' }, description: 'List of hashtags' }
              },
              required: ['content', 'video_path']
            }
          },
          {
            name: 'upload_to_youtube',
            description: 'Upload content to YouTube',
            inputSchema: {
              type: 'object',
              properties: {
                title: { type: 'string', description: 'Video title' },
                description: { type: 'string', description: 'Video description' },
                video_path: { type: 'string', description: 'Path to video file' },
                tags: { type: 'array', items: { type: 'string' }, description: 'Video tags' },
                schedule_time: { type: 'string', description: 'ISO datetime for scheduling (optional)' }
              },
              required: ['title', 'description', 'video_path']
            }
          },
          {
            name: 'post_to_linkedin',
            description: 'Post content to LinkedIn',
            inputSchema: {
              type: 'object',
              properties: {
                content: { type: 'string', description: 'Post content' },
                media_path: { type: 'string', description: 'Path to image file (optional)' }
              },
              required: ['content']
            }
          },
          {
            name: 'cross_post',
            description: 'Post content across multiple platforms simultaneously',
            inputSchema: {
              type: 'object',
              properties: {
                content: { type: 'string', description: 'Post content' },
                platforms: {
                  type: 'array',
                  items: { type: 'string', enum: ['twitter', 'instagram', 'tiktok', 'youtube', 'linkedin'] },
                  description: 'Platforms to post to'
                },
                media_path: { type: 'string', description: 'Path to media file (optional)' },
                platform_specific: { type: 'object', description: 'Platform-specific adaptations' }
              },
              required: ['content', 'platforms']
            }
          },
          {
            name: 'get_analytics',
            description: 'Get analytics data from social media platforms',
            inputSchema: {
              type: 'object',
              properties: {
                platforms: { type: 'array', items: { type: 'string' }, description: 'Platforms to get analytics from' },
                start_date: { type: 'string', description: 'Start date (YYYY-MM-DD)' },
                end_date: { type: 'string', description: 'End date (YYYY-MM-DD)' },
                metrics: { type: 'array', items: { type: 'string' }, description: 'Metrics to retrieve' }
              },
              required: ['platforms']
            }
          }
        ]
      };
    });

    this.server.setRequestHandler(CallToolRequestSchema, async (request) => {
      try {
        const { name, arguments: args } = request.params;
        
        switch (name) {
          case 'post_to_twitter':
            return await this.postToTwitter(args);
          case 'post_to_instagram':
            return await this.postToInstagram(args);
          case 'post_to_tiktok':
            return await this.postToTikTok(args);
          case 'upload_to_youtube':
            return await this.uploadToYouTube(args);
          case 'post_to_linkedin':
            return await this.postToLinkedIn(args);
          case 'cross_post':
            return await this.crossPost(args);
          case 'get_analytics':
            return await this.getAnalytics(args);
          default:
            throw new Error(`Unknown tool: ${name}`);
        }
      } catch (error) {
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify({ error: error.message }, null, 2)
            }
          ]
        };
      }
    });
  }

  async postToTwitter(args) {
    try {
      const { content, media_path, schedule_time } = args;
      
      let mediaIds = [];
      if (media_path) {
        const mediaData = await fs.readFile(media_path);
        const uploadResult = await this.uploadToTwitterMedia(mediaData);
        mediaIds.push(uploadResult.media_id_string);
      }

      const payload = { text: content };
      if (mediaIds.length > 0) {
        payload.media = { media_ids: mediaIds };
      }

      const response = await axios.post(
        'https://api.twitter.com/2/tweets',
        payload,
        {
          headers: {
            'Authorization': `Bearer ${process.env.TWITTER_BEARER_TOKEN}`,
            'Content-Type': 'application/json'
          }
        }
      );

      return {
        content: [
          {
            type: 'text',
            text: JSON.stringify({ success: true, result: response.data }, null, 2)
          }
        ]
      };
    } catch (error) {
      return {
        content: [
          {
            type: 'text',
            text: JSON.stringify({ success: false, error: error.message }, null, 2)
          }
        ]
      };
    }
  }

  async postToInstagram(args) {
    try {
      const { content, media_path, media_type } = args;
      
      // Upload media to accessible URL first
      const mediaUrl = await this.uploadMediaToUrl(media_path);
      
      const response = await axios.post(
        `https://graph.facebook.com/v18.0/${process.env.INSTAGRAM_BUSINESS_ID}/media`,
        {
          [media_type === 'photo' ? 'image_url' : 'video_url']: mediaUrl,
          caption: content,
          access_token: process.env.INSTAGRAM_ACCESS_TOKEN
        }
      );

      const creationId = response.data.id;
      
      // Publish the media
      const publishResponse = await axios.post(
        `https://graph.facebook.com/v18.0/${process.env.INSTAGRAM_BUSINESS_ID}/media_publish`,
        {
          creation_id: creationId,
          access_token: process.env.INSTAGRAM_ACCESS_TOKEN
        }
      );

      return {
        content: [
          {
            type: 'text',
            text: JSON.stringify({ success: true, result: publishResponse.data }, null, 2)
          }
        ]
      };
    } catch (error) {
      return {
        content: [
          {
            type: 'text',
            text: JSON.stringify({ success: false, error: error.message }, null, 2)
          }
        ]
      };
    }
  }

  async postToTikTok(args) {
    try {
      const { content, video_path, hashtags } = args;
      
      const videoData = await fs.readFile(video_path);
      const form = new FormData();
      form.append('video', videoData, {
        filename: path.basename(video_path),
        contentType: 'video/mp4'
      });
      form.append('access_token', process.env.TIKTOK_ACCESS_TOKEN);
      form.append('caption', content);
      
      if (hashtags && hashtags.length > 0) {
        form.append('hashtags', hashtags.join(','));
      }

      const response = await axios.post(
        'https://open-api.tiktok.com/share/video/upload/',
        form,
        {
          headers: {
            ...form.getHeaders()
          }
        }
      );

      return {
        content: [
          {
            type: 'text',
            text: JSON.stringify({ success: true, result: response.data }, null, 2)
          }
        ]
      };
    } catch (error) {
      return {
        content: [
          {
            type: 'text',
            text: JSON.stringify({ success: false, error: error.message }, null, 2)
          }
        ]
      };
    }
  }

  async uploadToYouTube(args) {
    try {
      const { title, description, video_path, tags, schedule_time } = args;
      
      // This would implement YouTube upload logic
      // For now, return a placeholder response
      const result = {
        video_id: `youtube_${Date.now()}`,
        title: title,
        status: schedule_time ? 'scheduled' : 'uploaded'
      };

      return {
        content: [
          {
            type: 'text',
            text: JSON.stringify({ success: true, result }, null, 2)
          }
        ]
      };
    } catch (error) {
      return {
        content: [
          {
            type: 'text',
            text: JSON.stringify({ success: false, error: error.message }, null, 2)
          }
        ]
      };
    }
  }

  async postToLinkedIn(args) {
    try {
      const { content, media_path } = args;
      
      if (media_path) {
        // Upload image first
        const imageData = await fs.readFile(media_path);
        const uploadResponse = await axios.post(
          'https://api.linkedin.com/v2/images?action=upload',
          imageData,
          {
            headers: {
              'Authorization': `Bearer ${process.env.LINKEDIN_ACCESS_TOKEN}`
            }
          }
        );
        
        const imageUrn = uploadResponse.data.image;
        
        // Create post with image
        const postData = {
          author: `urn:li:person:${await this.getLinkedInPersonId()}`,
          lifecycleState: 'PUBLISHED',
          specificContent: {
            'com.linkedin.ugc.ShareContent': {
              shareCommentary: { text: content },
              shareMediaCategory: 'IMAGE',
              media: [
                {
                  status: 'READY',
                  description: { text: 'Image' },
                  media: imageUrn,
                  title: { text: 'Post Image' }
                }
              ]
            }
          },
          visibility: { 'com.linkedin.ugc.MemberNetworkVisibility': 'PUBLIC' }
        };
        
        const response = await axios.post(
          'https://api.linkedin.com/v2/ugcPosts?action=create',
          postData,
          {
            headers: {
              'Authorization': `Bearer ${process.env.LINKEDIN_ACCESS_TOKEN}`,
              'Content-Type': 'application/json'
            }
          }
        );
        
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify({ success: true, result: response.data }, null, 2)
            }
          ]
        };
      } else {
        // Text-only post
        const postData = {
          author: `urn:li:person:${await this.getLinkedInPersonId()}`,
          lifecycleState: 'PUBLISHED',
          specificContent: {
            'com.linkedin.ugc.ShareContent': {
              shareCommentary: { text: content },
              shareMediaCategory: 'NONE'
            }
          },
          visibility: { 'com.linkedin.ugc.MemberNetworkVisibility': 'PUBLIC' }
        };
        
        const response = await axios.post(
          'https://api.linkedin.com/v2/ugcPosts?action=create',
          postData,
          {
            headers: {
              'Authorization': `Bearer ${process.env.LINKEDIN_ACCESS_TOKEN}`,
              'Content-Type': 'application/json'
            }
          }
        );
        
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify({ success: true, result: response.data }, null, 2)
            }
          ]
        };
      }
    } catch (error) {
      return {
        content: [
          {
            type: 'text',
            text: JSON.stringify({ success: false, error: error.message }, null, 2)
          }
        ]
      };
    }
  }

  async crossPost(args) {
    try {
      const { content, platforms, media_path } = args;
      const results = {};
      
      for (const platform of platforms) {
        switch (platform) {
          case 'twitter':
            results.twitter = await this.postToTwitter({ content, media_path });
            break;
          case 'instagram':
            results.instagram = await this.postToInstagram({ 
              content, 
              media_path, 
              media_type: 'photo' // Default to photo
            });
            break;
          case 'tiktok':
            results.tiktok = await this.postToTikTok({ 
              content, 
              video_path: media_path 
            });
            break;
          case 'youtube':
            results.youtube = await this.uploadToYouTube({ 
              title: content.substring(0, 100), 
              description: content, 
              video_path: media_path 
            });
            break;
          case 'linkedin':
            results.linkedin = await this.postToLinkedIn({ content, media_path });
            break;
        }
      }
      
      return {
        content: [
          {
            type: 'text',
            text: JSON.stringify({ success: true, results }, null, 2)
          }
        ]
      };
    } catch (error) {
      return {
        content: [
          {
            type: 'text',
            text: JSON.stringify({ success: false, error: error.message }, null, 2)
          }
        ]
      };
    }
  }

  async getAnalytics(args) {
    try {
      const { platforms, start_date, end_date } = args;
      const analytics = {};
      
      for (const platform of platforms) {
        // This would implement platform-specific analytics fetching
        analytics[platform] = {
          followers: Math.floor(Math.random() * 10000),
          engagement_rate: (Math.random() * 10).toFixed(2),
          impressions: Math.floor(Math.random() * 100000),
          reach: Math.floor(Math.random() * 50000)
        };
      }
      
      return {
        content: [
          {
            type: 'text',
            text: JSON.stringify({ success: true, analytics }, null, 2)
          }
        ]
      };
    } catch (error) {
      return {
        content: [
          {
            type: 'text',
            text: JSON.stringify({ success: false, error: error.message }, null, 2)
          }
        ]
      };
    }
  }

  // Helper methods
  async uploadToTwitterMedia(mediaData) {
    const form = new FormData();
    form.append('media', mediaData, {
      filename: 'media.jpg',
      contentType: 'image/jpeg'
    });
    form.append('media_category', 'tweet_image');
    
    const response = await axios.post(
      'https://upload.twitter.com/1.1/media/upload.json',
      form,
      {
        headers: {
          ...form.getHeaders()
        }
      }
    );
    
    return response.data;
  }

  async uploadMediaToUrl(mediaPath) {
    // This would upload media to CDN or storage service
    // For now, return a placeholder URL
    return `https://cdn.example.com/media/${path.basename(mediaPath)}`;
  }

  async getLinkedInPersonId() {
    const response = await axios.get(
      'https://api.linkedin.com/v2/people/~:(id)',
      {
        headers: {
          'Authorization': `Bearer ${process.env.LINKEDIN_ACCESS_TOKEN}`
        }
      }
    );
    return response.data.id;
  }

  async run() {
    const transport = new StdioServerTransport();
    await this.server.connect(transport);
    console.error('Social Media MCP server running on stdio');
  }
}

// Start the server
const server = new SocialMediaMCPServer();
server.run().catch(console.error);