require('dotenv').config(); // Load environment variables
const express = require('express');
const bodyParser = require('body-parser');
const mysql = require('mysql');

const app = express();
const port = 3306;

app.use(bodyParser.json());

// MySQL connection
const db = mysql.createConnection({
  host: process.env.DB_HOST,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  database: process.env.DB_NAME
});

db.connect(err => {
  if (err) {
    console.error('Error connecting to MySQL:', err);
    process.exit(1);
  }
  console.log('MySQL connected...');
});

// Drones Table
const TABLE_NAME = 'drones';

// Create a new record
app.post('/api/records', (req, res) => {
  const sql = `INSERT INTO ${TABLE_NAME} SET ?`;
  const newRecord = req.body;
  db.query(sql, newRecord, (err, result) => {
    if (err) {
      console.error('Error adding record:', err);
      return res.status(500).send('Error adding record');
    }
    res.send('Record added...');
  });
});

// Read all records
app.get('/api/records', (req, res) => {
  const sql = `SELECT * FROM ${TABLE_NAME}`;
  db.query(sql, (err, results) => {
    if (err) {
      console.error('Error fetching records:', err);
      return res.status(500).send('Error fetching records');
    }
    res.json(results);
  });
});

// Read a single record
app.get('/api/records/:id', (req, res) => {
  const sql = `SELECT * FROM ${TABLE_NAME} WHERE id = ?`;
  db.query(sql, [req.params.id], (err, result) => {
    if (err) {
      console.error('Error fetching record:', err);
      return res.status(500).send('Error fetching record');
    }
    res.json(result);
  });
});

// Update a record
app.put('/api/records/:id', (req, res) => {
  const sql = `UPDATE ${TABLE_NAME} SET ? WHERE id = ?`;
  const updatedRecord = req.body;
  db.query(sql, [updatedRecord, req.params.id], (err, result) => {
    if (err) {
      console.error('Error updating record:', err);
      return res.status(500).send('Error updating record');
    }
    res.send('Record updated...');
  });
});

// Delete a record
app.delete('/api/records/:id', (req, res) => {
  const sql = `DELETE FROM ${TABLE_NAME} WHERE id = ?`;
  db.query(sql, [req.params.id], (err, result) => {
    if (err) {
      console.error('Error deleting record:', err);
      return res.status(500).send('Error deleting record');
    }
    res.send('Record deleted...');
  });
});

app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});