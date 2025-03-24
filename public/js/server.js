require('dotenv').config(); // Load environment variables from .env
const express = require('express');
const bodyParser = require('body-parser');
const { Configuration, OpenAIApi } = require("openai");

const app = express();
const port = process.env.PORT || 3000;

// Configure OpenAI API with secret key (set in .env)
const configuration = new Configuration({
  apiKey: process.env.OPENAI_API_KEY,
});
const openai = new OpenAIApi(configuration);

// Middleware to parse JSON and serve static files from 'public'
app.use(bodyParser.json());
app.use(express.static('public'));

// API endpoint to get disposal advice
app.post('/api/disposal-advice', async (req, res) => {
  const { itemDescription } = req.body;
  if (!itemDescription) {
    return res.status(400).json({ error: 'Missing item description' });
  }
  
  try {
    // Call ChatGPT API with a system message and user query
    const response = await openai.createChatCompletion({
      model: "gpt-3.5-turbo",
      messages: [
        {
          role: "system",
          content:
            "You are a waste management expert. Provide clear instructions on how to dispose of items in the trash, recycling, or compost. Include explanations if needed.",
        },
        {
          role: "user",
          content: `How should I dispose of ${itemDescription}?`,
        },
      ],
    });
    
    const advice = response.data.choices[0].message.content;
    res.json({ advice });
  } catch (error) {
    console.error("Error getting disposal advice:", error);
    res.status(500).json({ error: 'Failed to get disposal advice' });
  }
});

// Start the server
app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});
