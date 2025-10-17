# Task 258 Analysis: Social Network Friendship Suggestions

## Problem Overview

This problem asks to count how many friendship suggestions should be sent in a social network. A suggestion is sent to user u to befriend user v if:

1. u and v are not already friends
2. There exists a mutual friend w who is friends with both u and v

## Key Difference: Problem Interpretation

### Normal Prompt Solution (Failed)

- **Approach**: Attempted to count unique friendship pairs that should be suggested
- **Implementation**: Used a set to store `(min(u,v), max(u,v))` pairs to avoid duplicates
- **Logic**: Grouped users by common friends, then suggested connections between pairs
- **Fatal Flaw**: Misinterpreted the problem as counting unique pairs rather than individual suggestions

### Test-Driven Prompt Solution (Passed)

- **Approach**: Counted individual suggestions sent to each user
- **Implementation**: Simple nested loop checking each user pair for common friends
- **Logic**: For each non-friend pair (u,v), check if they have a mutual friend w
- **Success**: Correctly interpreted that each suggestion is directional (u gets suggestion about v, AND v gets suggestion about u)

## Critical Insight: Directional vs. Bidirectional Counting

The example clarifies the counting semantics:

```
Input: 4 users, user 0 friends with users 1,2,3
Expected Output: 6

Breakdown:
- User 1 receives 2 suggestions: befriend user 2 (via user 0), befriend user 3 (via user 0)
- User 2 receives 2 suggestions: befriend user 1 (via user 0), befriend user 3 (via user 0)
- User 3 receives 2 suggestions: befriend user 1 (via user 0), befriend user 2 (via user 0)
- User 0 receives 0 suggestions (already friends with everyone)

Total: 6 individual suggestions sent
```

## Algorithm Comparison

### Failed Algorithm (Normal)

```python
# Tried to find unique pairs and count them once
for w in range(N):
    w_friends = [i for i in range(N) if friends[w][i] and i != w]
    for i in range(len(w_friends)):
        for j in range(i+1, len(w_friends)):
            u, v = w_friends[i], w_friends[j]
            if not friends[u][v]:
                suggestions.add((min(u,v), max(u,v)))  # Count pair once
```

### Successful Algorithm (TD)

```python
# Count each individual suggestion
for u in range(N):
    for v in range(N):
        if u == v or friends[u][v]:
            continue
        # Check if u and v have a common friend
        for w in range(N):
            if w != u and w != v and friends[u][w] and friends[v][w]:
                suggestions += 1  # Count suggestion to u about v
                break
```

## Impact of Test-Driven Development

The TD approach succeeded because:

1. **Immediate Validation**: Test cases provided concrete examples showing expected behavior
2. **Semantic Clarity**: Seeing output "6" instead of "3" revealed the directional nature of suggestions
3. **Iterative Refinement**: Could test assumptions against multiple examples and adjust logic accordingly
4. **Problem Disambiguation**: Tests helped distinguish between "friendship pairs to create" vs "suggestions to send"

## Conclusion

This case demonstrates how test-driven development helps with problem interpretation, especially when natural language descriptions can be ambiguous. The normal prompt solution was technically correct for one interpretation of the problem, but the test cases revealed the actual intended semantics. The TD approach's access to concrete examples prevented the fundamental misunderstanding that caused the normal solution to fail.
