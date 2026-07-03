# YouTube Video Scoring Rubric

This reference defines how to score and rank YouTube video candidates against user-supplied criteria, then how to report the pick. Part A is the scoring rubric. Part B is the report template.

## Part A: Scoring Rubric

Score each candidate on four dimensions, 0 to 5 each. Combine the four scores into one weighted score using the formula below. Relevance carries the most weight because a highly engaging video that misses the point is still the wrong pick.

### Dimensions and weights

| # | Dimension | Weight |
|---|-----------|--------|
| 1 | Relevance to criteria | 40% |
| 2 | Engagement quality | 30% |
| 3 | Comment sentiment | 20% |
| 4 | Constraint fit | 10% |

### 1. Relevance to criteria (40%)

How well the video matches the user's stated topic, purpose, and hard constraints.

| Score | Anchor |
|-------|--------|
| 5 | Directly and fully matches topic, purpose, and hard constraints |
| 4 | Matches topic and purpose well, small gaps against the finer intent |
| 3 | Matches the topic but misses some of the intent behind it |
| 2 | Loosely related, covers only part of the topic or purpose |
| 1 | Tangential, the topic only shows up in passing |
| 0 | Off-topic |

### 2. Engagement quality (30%)

YouTube hides public dislike counts, so judge engagement from what's actually visible: view count, like-to-view ratio, how recent the upload is relative to what the criteria call for, and channel authority (subscriber count, track record on the topic).

| Score | Anchor |
|-------|--------|
| 5 | Strong views, healthy like-to-view ratio, credible channel |
| 4 | Good on most signals, one signal is average rather than strong |
| 3 | Decent but mixed, some signals strong and others weak |
| 2 | Weak on most signals, one saving grace |
| 1 | Weak or thin signals across the board |
| 0 | Near-zero engagement, or signals that look manipulated |

### 3. Comment sentiment (20%)

Read the top comments. Weigh the ratio of praise to complaints, whether commenters confirm the video delivers on its title, and whether the praise or complaints are specific and recurring rather than generic.

| Score | Anchor |
|-------|--------|
| 5 | Overwhelmingly positive, comments confirm the video delivers real value |
| 4 | Mostly positive, minor recurring gripes that don't undercut the core value |
| 3 | Mixed, praise and complaints roughly balanced |
| 2 | Leaning negative, recurring specific complaints outweigh praise |
| 1 | Mostly negative, or repeated "clickbait" or "doesn't deliver" complaints |
| 0 | Comments disabled, or overwhelmingly negative |

### 4. Constraint fit (10%)

Hard constraints from the user's criteria: maximum length, language, upload recency window, channel preferences or exclusions.

| Score | Anchor |
|-------|--------|
| 5 | Meets every stated constraint |
| 4 | Meets every hard constraint, slight miss on a soft preference |
| 3 | Meets most constraints, one soft constraint missed |
| 2 | Meets the hard constraints, multiple soft constraints missed |
| 1 | Violates a soft constraint |
| 0 | Violates a hard constraint |

### Formula

```
weighted_score = 0.40 * relevance + 0.30 * engagement + 0.20 * comment_sentiment + 0.10 * constraint_fit
```

The result lands on a 0 to 5 scale.

### Disqualification rule

A score of 0 on constraint_fit for a HARD constraint (not a soft preference) disqualifies the candidate outright, no matter how the other three dimensions score. Don't average a hard-constraint violation into the total. Drop the candidate from the ranking entirely and note why in the report.

### Worked example

Criteria: topic "Docker Compose basics," purpose "set up a local dev environment," hard constraints: under 20 minutes, English, uploaded within the last 2 years.

Candidate: "Docker Compose Full Tutorial," 18 minutes, English, uploaded 8 months ago, 450K views, 22K likes (about 4.9% like-to-view ratio), channel has a strong track record on dev tutorials. Top comments run mostly positive, with a few noting the intro runs long.

| Dimension | Score | Why |
|-----------|-------|-----|
| Relevance | 5 | Covers the exact topic and purpose |
| Engagement | 4 | Strong views and ratio, credible channel, short of the strongest in the field |
| Comment sentiment | 4 | Mostly positive, one recurring minor gripe |
| Constraint fit | 5 | 18 minutes, English, 8 months old, every constraint met |

```
weighted_score = 0.40*5 + 0.30*4 + 0.20*4 + 0.10*5
              = 2.0 + 1.2 + 0.8 + 0.5
              = 4.5
```

This candidate scores 4.5 out of 5.

## Part B: Report Template

Fill in the placeholders below. Drop a section if it doesn't apply, for example skip "Runner-up" when only one candidate turned up.

Linking rule: every named video must be a clickable link to its canonical YouTube watch URL. Wherever a placeholder names a video, pair it with the URL, and carry links through any prose mention too.

```markdown
# YouTube pick: {topic}

## Criteria
- Topic: {topic}
- Purpose: {purpose}
- Constraints: {constraints}
- Session: {session_type} (logged-in or anonymous)

## Candidates

| Rank | Title | Channel | Views | Uploaded | Duration | Score | URL |
|------|-------|---------|-------|----------|----------|-------|-----|
| 1 | {candidate_1_title} | {candidate_1_channel} | {candidate_1_views} | {candidate_1_uploaded} | {candidate_1_duration} | {candidate_1_score} | {candidate_1_url} |
| 2 | {candidate_2_title} | {candidate_2_channel} | {candidate_2_views} | {candidate_2_uploaded} | {candidate_2_duration} | {candidate_2_score} | {candidate_2_url} |
| 3 | {candidate_3_title} | {candidate_3_channel} | {candidate_3_views} | {candidate_3_uploaded} | {candidate_3_duration} | {candidate_3_score} | {candidate_3_url} |

## Winner

[{winner_title}]({winner_url}), by {winner_channel}

{winner_reasoning}

## Rating breakdown

- Relevance: {winner_relevance_score}/5. {winner_relevance_note}
- Engagement quality: {winner_engagement_score}/5. {winner_engagement_note}
- Comment sentiment: {winner_sentiment_score}/5. {winner_sentiment_note}
- Constraint fit: {winner_constraint_score}/5. {winner_constraint_note}

## What viewers say

- Recurring praise: {recurring_praise}
- Recurring complaints: {recurring_complaints}
- Overall read: {sentiment_read}

## Runner-up

[{runnerup_title}]({runnerup_url}) came in second. {runnerup_reason_lost}

## Verdict

{verdict_sentence}
```
