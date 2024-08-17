const express = require('express');
const axios = require('axios');
const app = express();
const port = 9876;
const windowSize = 10; 
let numberWindow = [];
const authToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJNYXBDbGFpbXMiOnsiZXhwIjoxNzIzODc2Mzg4LCJpYXQiOjE3MjM4NzYwODgsImlzcyI6IkFmZm9yZG1lZCIsImp0aSI6IjhmMzIzYTIzLWEzYWEtNDlhNS1iZDM5LTFjZDc1NWEyYWFjNyIsInN1YiI6IjIxMTFjczAyMDUwOEBtYWxsYXJlZGR5dW5pdmVyc2l0eS5hYy5pbiJ9LCJjb21wYW55TmFtZSI6Ik1hbGxhIFJlZGR5IFVuaXZlcnNpdHkiLCJjbGllbnRJRCI6IjhmMzIzYTIzLWEzYWEtNDlhNS1iZDM5LTFjZDc1NWEyYWFjNyIsImNsaWVudFNlY3JldCI6IkNSdWtxclBmQnBPd1ZiWW8iLCJvd25lck5hbWUiOiJTaGl2YSBLdW1hciBZZWRsYSIsIm93bmVyRW1haWwiOiIyMTExY3MwMjA1MDhAbWFsbGFyZWRkeXVuaXZlcnNpdHkuYWMuaW4iLCJyb2xsTm8iOiIyMTExQ1MwMjA1MDgifQ.HwsJaGgpcuiS-Zet70YaGi-8uj8FqaUrJCCtQjGRO50'; 
const testServerUrls = {
  p: 'http://20.244.56.144/test/primes',
  T: 'http://20.244.56.144/test/Fibo',
  e: 'http://20.244.56.144/test/even',
  r: 'http://20.244.56.144/test/rand'
};
app.get('/numbers/:id', async (req, res) => {
  const id = req.params.id;
  if (!testServerUrls[id]) {
    return res.status(400).json({ error: 'Invalid ID' });
  }
  try {
    const response = await axios.get(testServerUrls[id], {
      headers: {
        'Authorization': `Bearer ${authToken}`
      },
      timeout: 500
    });
    const receivedNumbers = response.data.numbers;
    const uniqueNumbers = [...new Set(receivedNumbers)];
    const windowPrevState = [...numberWindow];
    numberWindow = [...numberWindow, ...uniqueNumbers];
    if (numberWindow.length > windowSize) {
      numberWindow = numberWindow.slice(-windowSize);
    }
    const sum = numberWindow.reduce((acc, num) => acc + num, 0);
    const avg = numberWindow.length ? (sum / numberWindow.length) : 0;
    res.json({
      numbers: uniqueNumbers,
      windowPrevState: windowPrevState,
      windowCurrState: numberWindow,
      avg: avg.toFixed(2)
    });
  } catch (error) {
    console.error("Error fetching numbers from the test server:", error.response ? error.response.data : error.message);
    res.status(500).json({ error: 'Failed to fetch numbers from the test server' });
  }
});
app.listen(port, () => {
  console.log(`Server running on http://localhost:${port}`);
});