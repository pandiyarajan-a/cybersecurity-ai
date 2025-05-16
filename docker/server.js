const express = require('express');
const app = express();
app.get('/', (req, res) => res.send('Vulnerable Node.js!'));
app.listen(3000);