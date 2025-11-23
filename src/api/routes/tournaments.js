const express = require('express');
const router = express.Router();
const db = require('../../../db');

router.get('/index', async (req, res) => {
  try {
    const allowedFields = [
      'index_id',
      'liquidpedia_url',
      'startgg_slug',
      'discovered_at',
      'processed'
    ];
    const fieldsParam = req.query.fields;
    const requestedFields = fieldsParam
      ? fieldsParam.split(',').map(f => f.trim())
      : allowedFields;
    const safeFields = requestedFields.filter(f => allowedFields.includes(f));

    if (safeFields.length === 0) {
      return res.status(400).json({ error: 'No valid fields requested' });
    }

    const sql = `SELECT ${safeFields.join(', ')} FROM tournament_index`;

    const result = await db.query(sql);
    res.json(result.rows);

  } catch (err) {
    console.error('Error fetching tournament index:', err);
    res.status(500).json({ error: 'Internal server error' });
  }
});

module.exports = router;