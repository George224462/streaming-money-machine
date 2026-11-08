-- ============================================================
-- PROJECT: The Streaming Money Machine
-- FILE: 01_exploratory_queries.sql
-- PURPOSE: Baseline financial and statistical queries on Spotify data
-- ============================================================

-- 1️⃣ QUERY 1: The "Rent-Paying" Genre Leaderboard
-- Question: Which genres generate the highest average revenue per track?
SELECT 
    track_genre,
    COUNT(*) AS total_tracks,
    ROUND(AVG(estimated_revenue_usd), 2) AS avg_revenue_per_track,
    ROUND(SUM(estimated_revenue_usd), 2) AS total_genre_revenue,
    ROUND(AVG(rent_months_covered), 2) AS avg_rent_months_per_track
FROM track_financials
GROUP BY track_genre
HAVING total_tracks >= 100
ORDER BY avg_revenue_per_track DESC
LIMIT 10;


-- 2️⃣ QUERY 2: Wealth Inequality in Music (The 1% vs. The 99%)
-- Question: How much of total streaming revenue goes to top-tier tracks?
WITH ranked_tracks AS (
    SELECT 
        track_name,
        track_artist,
        estimated_revenue_usd,
        NTILE(100) OVER (ORDER BY estimated_revenue_usd DESC) AS revenue_percentile
    FROM track_financials
)
SELECT 
    CASE 
        WHEN revenue_percentile = 1 THEN 'Top 1%'
        WHEN revenue_percentile <= 5 THEN 'Top 2-5%'
        WHEN revenue_percentile <= 10 THEN 'Top 6-10%'
        WHEN revenue_percentile <= 25 THEN 'Top 11-25%'
        WHEN revenue_percentile <= 50 THEN 'Top 26-50%'
        ELSE 'Bottom 50%'
    END AS artist_tier,
    COUNT(*) AS num_tracks,
    ROUND(SUM(estimated_revenue_usd), 2) AS total_revenue_usd,
    ROUND(AVG(estimated_revenue_usd), 2) AS avg_revenue_usd
FROM ranked_tracks
GROUP BY artist_tier
ORDER BY avg_revenue_usd DESC;


-- 3️⃣ QUERY 3: The "Explicit Premium"
-- Question: Does explicit language lead to higher popularity and revenue?
SELECT 
    CASE WHEN explicit = 1 THEN 'Explicit 🤬' ELSE 'Clean 😇' END AS track_type,
    COUNT(*) AS total_tracks,
    ROUND(AVG(track_popularity), 2) AS avg_popularity,
    ROUND(AVG(estimated_revenue_usd), 2) AS avg_revenue_usd,
    ROUND(AVG(danceability), 3) AS avg_danceability,
    ROUND(AVG(energy), 3) AS avg_energy
FROM track_financials
GROUP BY explicit;


-- 4️⃣ QUERY 4: Audio Profiles of Top vs. Bottom Earners
-- Question: What do high-earning songs sound like compared to low earners?
SELECT 
    'Top 10% Earners' AS track_tier,
    ROUND(AVG(duration_ms)/1000.0/60.0, 2) AS avg_duration_minutes,
    ROUND(AVG(danceability), 3) AS avg_danceability,
    ROUND(AVG(energy), 3) AS avg_energy,
    ROUND(AVG(tempo), 1) AS avg_tempo_bpm
FROM track_financials
WHERE track_popularity >= 70

UNION ALL

SELECT 
    'Bottom 50% Earners' AS track_tier,
    ROUND(AVG(duration_ms)/1000.0/60.0, 2) AS avg_duration_minutes,
    ROUND(AVG(danceability), 3) AS avg_danceability,
    ROUND(AVG(energy), 3) AS avg_energy,
    ROUND(AVG(tempo), 1) AS avg_tempo_bpm
FROM track_financials
WHERE track_popularity < 40;


-- 5️⃣ QUERY 5: The "Living Salary" Calculator ($50K Target)
-- Question: How many tracks does an artist need to publish to make $50,000/yr?
WITH tier_data AS (
    SELECT 
        CASE 
            WHEN track_popularity >= 80 THEN '🌟 Superstar (80-100)'
            WHEN track_popularity >= 60 THEN '🔥 Mainstream (60-79)'
            WHEN track_popularity >= 40 THEN '📈 Mid-Tier (40-59)'
            WHEN track_popularity >= 20 THEN '🌱 Underground (20-39)'
            ELSE '🔇 Unheard (0-19)'
        END AS artist_tier,
        AVG(estimated_revenue_usd) AS avg_revenue
    FROM track_financials
    GROUP BY artist_tier
)
SELECT 
    artist_tier,
    ROUND(avg_revenue, 2) AS avg_revenue_per_track_usd,
    CAST(ROUND(50000.0 / NULLIF(avg_revenue, 0)) AS INT) AS tracks_needed_for_50k_salary
FROM tier_data
ORDER BY avg_revenue DESC;