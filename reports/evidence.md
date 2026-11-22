# Evidence: cross-system timelines per request

## 01_baseline_kb / tr-10ba13e3

User: How do I connect to the VPN from home?

```
+ 0.00s  assistant request_received   {"message": "How do I connect to the VPN from home?", "llm": "offline-rules"}
+ 0.00s  assistant plan               {"action": "kb", "args": {}, "planner": "offline-rules"}
+ 0.00s  scenarios scenario_query     {"scenario": "01_baseline_kb", "description": "Healthy system, knowledge-base questions", "query": "How do I connect to the VPN from home?"}
+ 0.00s  assistant retrieval          {"top_k": 3, "chunk_size_words": 80, "results": [{"doc_id": "vpn-setup", "chunk_idx": 1, "score": 0.24, "updated": "2026-03-02", "words": 40}, {"doc_id": "vpn-setup", "chunk_idx": 0, "score": 0.224, "updated": "2026-03-02", "words": 80}, {"doc_id": "new-hire-equipment", "chunk_idx": 0, "score": 0.164, "updated": "2026-01-30", "words": 74}], "top_is_stale": false}
+ 0.00s  assistant answer             {"outcome": "answered", "citations": ["vpn-setup"], "answer": "According to 'Connect to the Corporate VPN (GlobalProtect)' (updated 2026-03-02): drops repeatedly, switch from Wi-Fi to a wired network and reconnect. If you see the error Gateway unreachable, check that your laptop clock is correct and contact the IT Service Desk. Do not use personal VPN software on company laptops."}
```

## 01_baseline_kb / tr-a06f77cc

User: I forgot my password, how do I reset it?

```
+ 0.00s  assistant request_received   {"message": "I forgot my password, how do I reset it?", "llm": "offline-rules"}
+ 0.00s  assistant plan               {"action": "kb", "args": {}, "planner": "offline-rules"}
+ 0.00s  scenarios scenario_query     {"scenario": "01_baseline_kb", "description": "Healthy system, knowledge-base questions", "query": "I forgot my password, how do I reset it?"}
+ 0.00s  assistant retrieval          {"top_k": 3, "chunk_size_words": 80, "results": [{"doc_id": "password-reset", "chunk_idx": 0, "score": 0.431, "updated": "2026-01-20", "words": 80}, {"doc_id": "password-reset", "chunk_idx": 1, "score": 0.21, "updated": "2026-01-20", "words": 31}, {"doc_id": "account-locked", "chunk_idx": 0, "score": 0.095, "updated": "2025-11-05", "words": 69}], "top_is_stale": false}
+ 0.00s  assistant answer             {"outcome": "answered", "citations": ["password-reset"], "answer": "According to 'Reset Your Password' (updated 2026-01-20): If you forgot your password, use the self-service portal at password.acme.example. Click Forgot password and verify your identity with an Okta Verify push or an SMS code. Choose a new password that is at least 14 characters long and that you have not used in your last 10 passwords. The new password syncs to email and your laptop within 15 minutes, so lock and unlock your laptop while connected to"}
```

## 01_baseline_kb / tr-69d4ad41

User: How do I request access to Salesforce?

```
+ 0.00s  assistant request_received   {"message": "How do I request access to Salesforce?", "llm": "offline-rules"}
+ 0.00s  assistant plan               {"action": "kb", "args": {}, "planner": "offline-rules"}
+ 0.00s  scenarios scenario_query     {"scenario": "01_baseline_kb", "description": "Healthy system, knowledge-base questions", "query": "How do I request access to Salesforce?"}
+ 0.00s  assistant retrieval          {"top_k": 3, "chunk_size_words": 80, "results": [{"doc_id": "salesforce-access", "chunk_idx": 0, "score": 0.561, "updated": "2026-02-24", "words": 69}, {"doc_id": "jira-access", "chunk_idx": 0, "score": 0.201, "updated": "2025-11-20", "words": 69}, {"doc_id": "shared-mailbox", "chunk_idx": 0, "score": 0.177, "updated": "2025-08-19", "words": 63}], "top_is_stale": false}
+ 0.00s  assistant answer             {"outcome": "answered", "citations": ["salesforce-access"], "answer": "According to 'Request Salesforce Access' (updated 2026-02-24): Request Salesforce access in the Access Portal and choose the role you need, either Sales Rep or Sales Manager. Your manager approves the request and you must have completed the Salesforce basics training first. After approval, access is provisioned through Okta within four business hours. The Salesforce tile then appears on your Okta dashboard. If the tile is missing after a day, open a ticket with your request number."}
```

## 02_baseline_tools / tr-db0a7c86

User: Create a ticket: my laptop screen is flickering

```
+ 0.00s  assistant request_received   {"message": "Create a ticket: my laptop screen is flickering", "llm": "offline-rules"}
+ 0.00s  assistant plan               {"action": "tool", "tool": "create_incident", "args": {"short_description": "my laptop screen is flickering"}, "planner": "offline-rules"}
+ 0.00s  scenarios scenario_query     {"scenario": "02_baseline_tools", "description": "Healthy system, ticket actions", "query": "Create a ticket: my laptop screen is flickering"}
+ 0.00s  api       http_request       {"method": "POST", "path": "/api/now/table/incident", "status": 201, "latency_ms": 1, "fault_mode": "none"}
+ 0.00s  assistant tool_call          {"tool": "create_incident", "attempt": 1, "method": "POST", "url": "http://127.0.0.1:8099/api/now/table/incident", "args_sent": {"short_description": "my laptop screen is flickering"}, "status": 201, "latency_ms": 3}
+ 0.00s  assistant answer             {"outcome": "ok", "tool": "create_incident", "http_status": 201, "attempts": 1, "answer": "I've created INC0010002: my laptop screen is flickering."}
```

## 02_baseline_tools / tr-2df5047e

User: What's the status of INC0004521?

```
+ 0.00s  assistant request_received   {"message": "What's the status of INC0004521?", "llm": "offline-rules"}
+ 0.00s  assistant plan               {"action": "tool", "tool": "get_incident", "args": {"number": "INC0004521"}, "planner": "offline-rules"}
+ 0.00s  scenarios scenario_query     {"scenario": "02_baseline_tools", "description": "Healthy system, ticket actions", "query": "What's the status of INC0004521?"}
+ 0.00s  api       http_request       {"method": "GET", "path": "/api/now/table/incident/INC0004521", "status": 200, "latency_ms": 1, "fault_mode": "none"}
+ 0.00s  assistant tool_call          {"tool": "get_incident", "attempt": 1, "method": "GET", "url": "http://127.0.0.1:8099/api/now/table/incident/INC0004521", "args_sent": {"number": "INC0004521"}, "status": 200, "latency_ms": 2}
+ 0.00s  assistant answer             {"outcome": "ok", "tool": "get_incident", "http_status": 200, "attempts": 1, "answer": "INC0004521 - Outlook keeps asking for password. Status: In Progress."}
```

## 02_baseline_tools / tr-9398650d

User: Update INC0004521: user confirmed the issue persists after reboot

```
+ 0.00s  scenarios scenario_query     {"scenario": "02_baseline_tools", "description": "Healthy system, ticket actions", "query": "Update INC0004521: user confirmed the issue persists after reboot"}
+ 0.00s  assistant request_received   {"message": "Update INC0004521: user confirmed the issue persists after reboot", "llm": "offline-rules"}
+ 0.00s  assistant plan               {"action": "tool", "tool": "update_incident", "args": {"number": "INC0004521", "work_notes": "user confirmed the issue persists after reboot"}, "planner": "offline-rules"}
+ 0.00s  api       http_request       {"method": "PATCH", "path": "/api/now/table/incident/INC0004521", "status": 200, "latency_ms": 1, "fault_mode": "none"}
+ 0.00s  assistant tool_call          {"tool": "update_incident", "attempt": 1, "method": "PATCH", "url": "http://127.0.0.1:8099/api/now/table/incident/INC0004521", "args_sent": {"number": "INC0004521", "work_notes": "user confirmed the issue persists after reboot"}, "status": 200, "latency_ms": 3}
+ 0.00s  assistant answer             {"outcome": "ok", "tool": "update_incident", "http_status": 200, "attempts": 1, "answer": "I've added your note to INC0004521."}
```

## 03_vpn_answer_wrong / tr-fc4ba193

User: How do I connect to the VPN from home?

```
+ 0.00s  assistant request_received   {"message": "How do I connect to the VPN from home?", "llm": "offline-rules"}
+ 0.00s  scenarios scenario_query     {"scenario": "03_vpn_answer_wrong", "description": "Customer reports the assistant gave outdated VPN instructions", "query": "How do I connect to the VPN from home?"}
+ 0.00s  assistant plan               {"action": "kb", "args": {}, "planner": "offline-rules"}
+ 0.00s  assistant retrieval          {"top_k": 3, "chunk_size_words": 80, "results": [{"doc_id": "vpn-setup-legacy", "chunk_idx": 0, "score": 0.56, "updated": "2022-03-14", "words": 76}, {"doc_id": "vpn-setup", "chunk_idx": 1, "score": 0.229, "updated": "2026-03-02", "words": 40}, {"doc_id": "vpn-setup", "chunk_idx": 0, "score": 0.215, "updated": "2026-03-02", "words": 80}], "conflicts": {"vpn": {"vpn-setup-legacy": "2022-03-14", "vpn-setup": "2026-03-02"}}, "top_is_stale": true}
+ 0.00s  assistant answer             {"outcome": "answered", "citations": ["vpn-setup-legacy"], "answer": "According to 'Connect to the VPN from Home (Cisco AnyConnect)' (updated 2022-03-14): To connect to the VPN from home, open Cisco AnyConnect and connect to vpn-old.acme.example. Enter your network username and password, then your RSA token code. The VPN client is installed by default on all laptops. Once the VPN shows connected you can reach the intranet and file shares from home. If you cannot connect to the VPN from home, restart AnyConnect and try the VPN again. Home users should always"}
```

## 04_vpn_answer_retest / tr-07244bed

User: How do I connect to the VPN from home?

```
+ 0.00s  assistant request_received   {"message": "How do I connect to the VPN from home?", "llm": "offline-rules"}
+ 0.00s  assistant plan               {"action": "kb", "args": {}, "planner": "offline-rules"}
+ 0.00s  scenarios scenario_query     {"scenario": "04_vpn_answer_retest", "description": "Retest of 03 after a configuration change", "query": "How do I connect to the VPN from home?"}
+ 0.00s  assistant conflict_resolved  {"original_top": "vpn-setup-legacy", "preferred": "vpn-setup", "rule": "newest_updated"}
+ 0.00s  assistant retrieval          {"top_k": 3, "chunk_size_words": 80, "results": [{"doc_id": "vpn-setup", "chunk_idx": 1, "score": 0.229, "updated": "2026-03-02", "words": 40}, {"doc_id": "vpn-setup-legacy", "chunk_idx": 0, "score": 0.56, "updated": "2022-03-14", "words": 76}, {"doc_id": "vpn-setup", "chunk_idx": 0, "score": 0.215, "updated": "2026-03-02", "words": 80}], "conflicts": {"vpn": {"vpn-setup-legacy": "2022-03-14", "vpn-setup": "2026-03-02"}}, "top_is_stale": false}
+ 0.00s  assistant answer             {"outcome": "answered", "citations": ["vpn-setup"], "answer": "According to 'Connect to the Corporate VPN (GlobalProtect)' (updated 2026-03-02): drops repeatedly, switch from Wi-Fi to a wired network and reconnect. If you see the error Gateway unreachable, check that your laptop clock is correct and contact the IT Service Desk. Do not use personal VPN software on company laptops."}
```

## 05_answers_incomplete / tr-0e2fa4dd

User: How do I connect to the VPN from home?

```
+ 0.00s  assistant request_received   {"message": "How do I connect to the VPN from home?", "llm": "offline-rules"}
+ 0.00s  assistant plan               {"action": "kb", "args": {}, "planner": "offline-rules"}
+ 0.00s  scenarios scenario_query     {"scenario": "05_answers_incomplete", "description": "Customer reports answers are cut off / useless after a re-index", "query": "How do I connect to the VPN from home?"}
+ 0.00s  assistant retrieval          {"top_k": 3, "chunk_size_words": 12, "results": [{"doc_id": "vpn-setup", "chunk_idx": 0, "score": 0.374, "updated": "2026-03-02", "words": 12}, {"doc_id": "vpn-setup", "chunk_idx": 8, "score": 0.305, "updated": "2026-03-02", "words": 4}, {"doc_id": "vpn-setup", "chunk_idx": 7, "score": 0.303, "updated": "2026-03-02", "words": 12}], "top_is_stale": false}
+ 0.00s  assistant answer             {"outcome": "answered", "citations": ["vpn-setup"], "answer": "According to 'Connect to the Corporate VPN (GlobalProtect)' (updated 2026-03-02): To work remotely you must connect to the corporate VPN using the"}
```

## 05_answers_incomplete / tr-98e784c7

User: I forgot my password, how do I reset it?

```
+ 0.00s  scenarios scenario_query     {"scenario": "05_answers_incomplete", "description": "Customer reports answers are cut off / useless after a re-index", "query": "I forgot my password, how do I reset it?"}
+ 0.00s  assistant request_received   {"message": "I forgot my password, how do I reset it?", "llm": "offline-rules"}
+ 0.00s  assistant plan               {"action": "kb", "args": {}, "planner": "offline-rules"}
+ 0.00s  assistant retrieval          {"top_k": 3, "chunk_size_words": 12, "results": [{"doc_id": "password-reset", "chunk_idx": 1, "score": 0.622, "updated": "2026-01-20", "words": 12}, {"doc_id": "password-reset", "chunk_idx": 0, "score": 0.576, "updated": "2026-01-20", "words": 12}, {"doc_id": "password-reset", "chunk_idx": 2, "score": 0.35, "updated": "2026-01-20", "words": 12}], "top_is_stale": false}
+ 0.00s  assistant answer             {"outcome": "answered", "citations": ["password-reset"], "answer": "According to 'Reset Your Password' (updated 2026-01-20): Forgot password and verify your identity with an Okta Verify push or"}
```

## 05_answers_incomplete / tr-572f1eb1

User: How do I request access to Salesforce?

```
+ 0.00s  assistant request_received   {"message": "How do I request access to Salesforce?", "llm": "offline-rules"}
+ 0.00s  assistant plan               {"action": "kb", "args": {}, "planner": "offline-rules"}
+ 0.00s  scenarios scenario_query     {"scenario": "05_answers_incomplete", "description": "Customer reports answers are cut off / useless after a re-index", "query": "How do I request access to Salesforce?"}
+ 0.00s  assistant retrieval          {"top_k": 3, "chunk_size_words": 12, "results": [{"doc_id": "salesforce-access", "chunk_idx": 0, "score": 0.773, "updated": "2026-02-24", "words": 12}, {"doc_id": "salesforce-access", "chunk_idx": 3, "score": 0.642, "updated": "2026-02-24", "words": 12}, {"doc_id": "salesforce-access", "chunk_idx": 5, "score": 0.589, "updated": "2026-02-24", "words": 9}], "top_is_stale": false}
+ 0.00s  assistant answer             {"outcome": "answered", "citations": ["salesforce-access"], "answer": "According to 'Request Salesforce Access' (updated 2026-02-24): Request Salesforce access in the Access Portal and choose the role you"}
```

## 06_answers_retest / tr-2eb7eef8

User: How do I connect to the VPN from home?

```
+ 0.00s  assistant request_received   {"message": "How do I connect to the VPN from home?", "llm": "offline-rules"}
+ 0.00s  assistant plan               {"action": "kb", "args": {}, "planner": "offline-rules"}
+ 0.00s  scenarios scenario_query     {"scenario": "06_answers_retest", "description": "Retest of 05 after reverting the re-index settings", "query": "How do I connect to the VPN from home?"}
+ 0.00s  assistant retrieval          {"top_k": 3, "chunk_size_words": 80, "results": [{"doc_id": "vpn-setup", "chunk_idx": 1, "score": 0.24, "updated": "2026-03-02", "words": 40}, {"doc_id": "vpn-setup", "chunk_idx": 0, "score": 0.224, "updated": "2026-03-02", "words": 80}, {"doc_id": "new-hire-equipment", "chunk_idx": 0, "score": 0.164, "updated": "2026-01-30", "words": 74}], "top_is_stale": false}
+ 0.00s  assistant answer             {"outcome": "answered", "citations": ["vpn-setup"], "answer": "According to 'Connect to the Corporate VPN (GlobalProtect)' (updated 2026-03-02): drops repeatedly, switch from Wi-Fi to a wired network and reconnect. If you see the error Gateway unreachable, check that your laptop clock is correct and contact the IT Service Desk. Do not use personal VPN software on company laptops."}
```

## 06_answers_retest / tr-0f4ee70c

User: I forgot my password, how do I reset it?

```
+ 0.00s  assistant request_received   {"message": "I forgot my password, how do I reset it?", "llm": "offline-rules"}
+ 0.00s  assistant plan               {"action": "kb", "args": {}, "planner": "offline-rules"}
+ 0.00s  scenarios scenario_query     {"scenario": "06_answers_retest", "description": "Retest of 05 after reverting the re-index settings", "query": "I forgot my password, how do I reset it?"}
+ 0.00s  assistant retrieval          {"top_k": 3, "chunk_size_words": 80, "results": [{"doc_id": "password-reset", "chunk_idx": 0, "score": 0.431, "updated": "2026-01-20", "words": 80}, {"doc_id": "password-reset", "chunk_idx": 1, "score": 0.21, "updated": "2026-01-20", "words": 31}, {"doc_id": "account-locked", "chunk_idx": 0, "score": 0.095, "updated": "2025-11-05", "words": 69}], "top_is_stale": false}
+ 0.00s  assistant answer             {"outcome": "answered", "citations": ["password-reset"], "answer": "According to 'Reset Your Password' (updated 2026-01-20): If you forgot your password, use the self-service portal at password.acme.example. Click Forgot password and verify your identity with an Okta Verify push or an SMS code. Choose a new password that is at least 14 characters long and that you have not used in your last 10 passwords. The new password syncs to email and your laptop within 15 minutes, so lock and unlock your laptop while connected to"}
```

## 06_answers_retest / tr-e7fbd9d9

User: How do I request access to Salesforce?

```
+ 0.00s  assistant request_received   {"message": "How do I request access to Salesforce?", "llm": "offline-rules"}
+ 0.00s  assistant plan               {"action": "kb", "args": {}, "planner": "offline-rules"}
+ 0.00s  scenarios scenario_query     {"scenario": "06_answers_retest", "description": "Retest of 05 after reverting the re-index settings", "query": "How do I request access to Salesforce?"}
+ 0.00s  assistant retrieval          {"top_k": 3, "chunk_size_words": 80, "results": [{"doc_id": "salesforce-access", "chunk_idx": 0, "score": 0.561, "updated": "2026-02-24", "words": 69}, {"doc_id": "jira-access", "chunk_idx": 0, "score": 0.201, "updated": "2025-11-20", "words": 69}, {"doc_id": "shared-mailbox", "chunk_idx": 0, "score": 0.177, "updated": "2025-08-19", "words": 63}], "top_is_stale": false}
+ 0.00s  assistant answer             {"outcome": "answered", "citations": ["salesforce-access"], "answer": "According to 'Request Salesforce Access' (updated 2026-02-24): Request Salesforce access in the Access Portal and choose the role you need, either Sales Rep or Sales Manager. Your manager approves the request and you must have completed the Salesforce basics training first. After approval, access is provisioned through Okta within four business hours. The Salesforce tile then appears on your Okta dashboard. If the tile is missing after a day, open a ticket with your request number."}
```

## 07_tickets_all_failing / tr-9c11c567

User: Create a ticket: my laptop screen is flickering

```
+ 0.00s  assistant request_received   {"message": "Create a ticket: my laptop screen is flickering", "llm": "offline-rules"}
+ 0.00s  assistant plan               {"action": "tool", "tool": "create_incident", "args": {"short_description": "my laptop screen is flickering"}, "planner": "offline-rules"}
+ 0.00s  scenarios scenario_query     {"scenario": "07_tickets_all_failing", "description": "Customer reports every ticket action fails since this morning", "query": "Create a ticket: my laptop screen is flickering"}
+ 0.00s  api       error_response     {"status": 401, "message": "User Not Authenticated", "detail": "Required to provide Auth information", "fault_mode": "auth_expired"}
+ 0.00s  api       http_request       {"method": "POST", "path": "/api/now/table/incident", "status": 401, "latency_ms": 0, "fault_mode": "auth_expired"}
+ 0.00s  assistant tool_call          {"tool": "create_incident", "attempt": 1, "method": "POST", "url": "http://127.0.0.1:8099/api/now/table/incident", "args_sent": {"short_description": "my laptop screen is flickering"}, "status": 401, "latency_ms": 2, "body_excerpt": "{\"error\":{\"message\":\"User Not Authenticated\",\"detail\":\"Required to provide Auth information\"},\"status\":\"failure\"}"}
+ 0.00s  assistant answer             {"outcome": "auth_failed", "tool": "create_incident", "http_status": 401, "attempts": 1, "answer": "I couldn't complete that: the ServiceNow integration rejected our credentials. (ref tr-9c11c567)"}
```

## 07_tickets_all_failing / tr-cdfe7d71

User: What's the status of INC0004521?

```
+ 0.00s  scenarios scenario_query     {"scenario": "07_tickets_all_failing", "description": "Customer reports every ticket action fails since this morning", "query": "What's the status of INC0004521?"}
+ 0.00s  assistant request_received   {"message": "What's the status of INC0004521?", "llm": "offline-rules"}
+ 0.00s  assistant plan               {"action": "tool", "tool": "get_incident", "args": {"number": "INC0004521"}, "planner": "offline-rules"}
+ 0.00s  api       error_response     {"status": 401, "message": "User Not Authenticated", "detail": "Required to provide Auth information", "fault_mode": "auth_expired"}
+ 0.00s  api       http_request       {"method": "GET", "path": "/api/now/table/incident/INC0004521", "status": 401, "latency_ms": 1, "fault_mode": "auth_expired"}
+ 0.00s  assistant tool_call          {"tool": "get_incident", "attempt": 1, "method": "GET", "url": "http://127.0.0.1:8099/api/now/table/incident/INC0004521", "args_sent": {"number": "INC0004521"}, "status": 401, "latency_ms": 2, "body_excerpt": "{\"error\":{\"message\":\"User Not Authenticated\",\"detail\":\"Required to provide Auth information\"},\"status\":\"failure\"}"}
+ 0.00s  assistant answer             {"outcome": "auth_failed", "tool": "get_incident", "http_status": 401, "attempts": 1, "answer": "I couldn't complete that: the ServiceNow integration rejected our credentials. (ref tr-cdfe7d71)"}
```

## 08_tickets_intermittent / tr-667d852a

User: What's the status of INC0004521?

```
+ 0.00s  assistant request_received   {"message": "What's the status of INC0004521?", "llm": "offline-rules"}
+ 0.00s  assistant plan               {"action": "tool", "tool": "get_incident", "args": {"number": "INC0004521"}, "planner": "offline-rules"}
+ 0.00s  scenarios scenario_query     {"scenario": "08_tickets_intermittent", "description": "Customer reports ticket lookups are flaky", "query": "What's the status of INC0004521?"}
+ 0.00s  api       error_response     {"status": 429, "message": "Too Many Requests", "detail": "Rate limit exceeded", "fault_mode": "rate_limit_first2"}
+ 0.00s  api       http_request       {"method": "GET", "path": "/api/now/table/incident/INC0004521", "status": 429, "latency_ms": 1, "fault_mode": "rate_limit_first2"}
+ 0.00s  assistant tool_call          {"tool": "get_incident", "attempt": 1, "method": "GET", "url": "http://127.0.0.1:8099/api/now/table/incident/INC0004521", "args_sent": {"number": "INC0004521"}, "status": 429, "latency_ms": 2, "body_excerpt": "{\"error\":{\"message\":\"Too Many Requests\",\"detail\":\"Rate limit exceeded\"},\"status\":\"failure\"}"}
+ 0.00s  assistant retry_scheduled    {"tool": "get_incident", "reason": 429, "retry_after_header": "1", "delay_s": 1.0}
+ 1.01s  api       error_response     {"status": 429, "message": "Too Many Requests", "detail": "Rate limit exceeded", "fault_mode": "rate_limit_first2"}
+ 1.01s  api       http_request       {"method": "GET", "path": "/api/now/table/incident/INC0004521", "status": 429, "latency_ms": 1, "fault_mode": "rate_limit_first2"}
+ 1.01s  assistant tool_call          {"tool": "get_incident", "attempt": 2, "method": "GET", "url": "http://127.0.0.1:8099/api/now/table/incident/INC0004521", "args_sent": {"number": "INC0004521"}, "status": 429, "latency_ms": 4, "body_excerpt": "{\"error\":{\"message\":\"Too Many Requests\",\"detail\":\"Rate limit exceeded\"},\"status\":\"failure\"}"}
+ 1.01s  assistant retry_scheduled    {"tool": "get_incident", "reason": 429, "retry_after_header": "1", "delay_s": 1.0}
+ 2.01s  api       http_request       {"method": "GET", "path": "/api/now/table/incident/INC0004521", "status": 200, "latency_ms": 1, "fault_mode": "rate_limit_first2"}
+ 2.01s  assistant tool_call          {"tool": "get_incident", "attempt": 3, "method": "GET", "url": "http://127.0.0.1:8099/api/now/table/incident/INC0004521", "args_sent": {"number": "INC0004521"}, "status": 200, "latency_ms": 5}
+ 2.01s  assistant answer             {"outcome": "ok", "tool": "get_incident", "http_status": 200, "attempts": 3, "answer": "INC0004521 - Outlook keeps asking for password. Status: In Progress."}
```

## 09_tickets_busy_all_day / tr-ecfbb7a3

User: What's the status of INC0004521?

```
+ 0.00s  assistant request_received   {"message": "What's the status of INC0004521?", "llm": "offline-rules"}
+ 0.00s  assistant plan               {"action": "tool", "tool": "get_incident", "args": {"number": "INC0004521"}, "planner": "offline-rules"}
+ 0.00s  scenarios scenario_query     {"scenario": "09_tickets_busy_all_day", "description": "Customer reports ticket lookups never work during a bulk import", "query": "What's the status of INC0004521?"}
+ 0.00s  api       error_response     {"status": 429, "message": "Too Many Requests", "detail": "Rate limit exceeded", "fault_mode": "rate_limit"}
+ 0.00s  api       http_request       {"method": "GET", "path": "/api/now/table/incident/INC0004521", "status": 429, "latency_ms": 1, "fault_mode": "rate_limit"}
+ 0.00s  assistant tool_call          {"tool": "get_incident", "attempt": 1, "method": "GET", "url": "http://127.0.0.1:8099/api/now/table/incident/INC0004521", "args_sent": {"number": "INC0004521"}, "status": 429, "latency_ms": 3, "body_excerpt": "{\"error\":{\"message\":\"Too Many Requests\",\"detail\":\"Rate limit exceeded\"},\"status\":\"failure\"}"}
+ 0.00s  assistant retry_scheduled    {"tool": "get_incident", "reason": 429, "retry_after_header": "1", "delay_s": 1.0}
+ 1.01s  api       error_response     {"status": 429, "message": "Too Many Requests", "detail": "Rate limit exceeded", "fault_mode": "rate_limit"}
+ 1.01s  api       http_request       {"method": "GET", "path": "/api/now/table/incident/INC0004521", "status": 429, "latency_ms": 1, "fault_mode": "rate_limit"}
+ 1.01s  assistant tool_call          {"tool": "get_incident", "attempt": 2, "method": "GET", "url": "http://127.0.0.1:8099/api/now/table/incident/INC0004521", "args_sent": {"number": "INC0004521"}, "status": 429, "latency_ms": 4, "body_excerpt": "{\"error\":{\"message\":\"Too Many Requests\",\"detail\":\"Rate limit exceeded\"},\"status\":\"failure\"}"}
+ 1.01s  assistant retry_scheduled    {"tool": "get_incident", "reason": 429, "retry_after_header": "1", "delay_s": 1.0}
+ 2.01s  api       error_response     {"status": 429, "message": "Too Many Requests", "detail": "Rate limit exceeded", "fault_mode": "rate_limit"}
+ 2.01s  api       http_request       {"method": "GET", "path": "/api/now/table/incident/INC0004521", "status": 429, "latency_ms": 1, "fault_mode": "rate_limit"}
+ 2.01s  assistant tool_call          {"tool": "get_incident", "attempt": 3, "method": "GET", "url": "http://127.0.0.1:8099/api/now/table/incident/INC0004521", "args_sent": {"number": "INC0004521"}, "status": 429, "latency_ms": 3, "body_excerpt": "{\"error\":{\"message\":\"Too Many Requests\",\"detail\":\"Rate limit exceeded\"},\"status\":\"failure\"}"}
+ 2.01s  assistant answer             {"outcome": "rate_limited", "tool": "get_incident", "http_status": 429, "attempts": 3, "answer": "ServiceNow is busy right now and I couldn't complete that. Please try again shortly. (ref tr-ecfbb7a3)"}
```

## 10_ticket_not_found / tr-58a27228

User: What's the status of ticket 4521?

```
+ 0.00s  assistant request_received   {"message": "What's the status of ticket 4521?", "llm": "offline-rules"}
+ 0.00s  assistant plan               {"action": "tool", "tool": "get_incident", "args": {"number": "4521"}, "planner": "offline-rules"}
+ 0.00s  scenarios scenario_query     {"scenario": "10_ticket_not_found", "description": "Customer says a ticket that exists is reported as not found", "query": "What's the status of ticket 4521?"}
+ 0.00s  api       error_response     {"status": 404, "message": "No Record found", "detail": "Record doesn't exist or ACL restricts the record retrieval", "fault_mode": "none"}
+ 0.00s  api       http_request       {"method": "GET", "path": "/api/now/table/incident/4521", "status": 404, "latency_ms": 1, "fault_mode": "none"}
+ 0.00s  assistant tool_call          {"tool": "get_incident", "attempt": 1, "method": "GET", "url": "http://127.0.0.1:8099/api/now/table/incident/4521", "args_sent": {"number": "4521"}, "status": 404, "latency_ms": 2, "body_excerpt": "{\"error\":{\"message\":\"No Record found\",\"detail\":\"Record doesn't exist or ACL restricts the record retrieval\"},\"status\":\"failure\"}"}
+ 0.00s  assistant answer             {"outcome": "not_found", "tool": "get_incident", "http_status": 404, "attempts": 1, "answer": "I couldn't find that ticket. Please double-check the number. (ref tr-58a27228)"}
```

## 11_not_found_retest / tr-2346f4b1

User: What's the status of ticket 4521?

```
+ 0.00s  scenarios scenario_query     {"scenario": "11_not_found_retest", "description": "Retest of 10 after a configuration change", "query": "What's the status of ticket 4521?"}
+ 0.00s  assistant request_received   {"message": "What's the status of ticket 4521?", "llm": "offline-rules"}
+ 0.00s  assistant plan               {"action": "tool", "tool": "get_incident", "args": {"number": "4521"}, "planner": "offline-rules"}
+ 0.00s  assistant arg_normalized     {"arg": "number", "before": "4521", "after": "INC0004521"}
+ 0.01s  api       http_request       {"method": "GET", "path": "/api/now/table/incident/INC0004521", "status": 200, "latency_ms": 3, "fault_mode": "none"}
+ 0.01s  assistant tool_call          {"tool": "get_incident", "attempt": 1, "method": "GET", "url": "http://127.0.0.1:8099/api/now/table/incident/INC0004521", "args_sent": {"number": "INC0004521"}, "status": 200, "latency_ms": 10}
+ 0.01s  assistant answer             {"outcome": "ok", "tool": "get_incident", "http_status": 200, "attempts": 1, "answer": "INC0004521 - Outlook keeps asking for password. Status: In Progress."}
```

## 12_after_api_upgrade / tr-cc22bc61

User: Create a ticket: my laptop screen is flickering

```
+ 0.00s  assistant request_received   {"message": "Create a ticket: my laptop screen is flickering", "llm": "offline-rules"}
+ 0.00s  assistant plan               {"action": "tool", "tool": "create_incident", "args": {"short_description": "my laptop screen is flickering"}, "planner": "offline-rules"}
+ 0.00s  scenarios scenario_query     {"scenario": "12_after_api_upgrade", "description": "Ticket actions broke right after ServiceNow upgraded the instance", "query": "Create a ticket: my laptop screen is flickering"}
+ 0.00s  api       error_response     {"status": 422, "message": "Invalid request", "detail": "Field 'summary' is required", "fault_mode": "schema_v2"}
+ 0.00s  api       http_request       {"method": "POST", "path": "/api/now/table/incident", "status": 422, "latency_ms": 1, "fault_mode": "schema_v2"}
+ 0.00s  assistant tool_call          {"tool": "create_incident", "attempt": 1, "method": "POST", "url": "http://127.0.0.1:8099/api/now/table/incident", "args_sent": {"short_description": "my laptop screen is flickering"}, "status": 422, "latency_ms": 2, "body_excerpt": "{\"error\":{\"message\":\"Invalid request\",\"detail\":\"Field 'summary' is required\"},\"status\":\"failure\"}"}
+ 0.00s  assistant answer             {"outcome": "bad_request", "tool": "create_incident", "http_status": 422, "attempts": 1, "answer": "ServiceNow rejected the request I sent, so nothing was changed. (ref tr-cc22bc61)"}
```

## 12_after_api_upgrade / tr-9f266766

User: What's the status of INC0004521?

```
+ 0.00s  assistant request_received   {"message": "What's the status of INC0004521?", "llm": "offline-rules"}
+ 0.00s  scenarios scenario_query     {"scenario": "12_after_api_upgrade", "description": "Ticket actions broke right after ServiceNow upgraded the instance", "query": "What's the status of INC0004521?"}
+ 0.00s  assistant plan               {"action": "tool", "tool": "get_incident", "args": {"number": "INC0004521"}, "planner": "offline-rules"}
+ 0.00s  api       http_request       {"method": "GET", "path": "/api/now/table/incident/INC0004521", "status": 200, "latency_ms": 1, "fault_mode": "schema_v2"}
+ 0.00s  assistant tool_call          {"tool": "get_incident", "attempt": 1, "method": "GET", "url": "http://127.0.0.1:8099/api/now/table/incident/INC0004521", "args_sent": {"number": "INC0004521"}, "status": 200, "latency_ms": 2}
+ 0.00s  assistant schema_mismatch    {"tool": "get_incident", "missing_fields": ["short_description", "state"], "fields_present": ["number", "status", "summary", "urgency", "work_notes"]}
+ 0.00s  assistant answer             {"outcome": "schema_mismatch", "tool": "get_incident", "http_status": 200, "attempts": 1, "answer": "ServiceNow replied in a format I didn't expect, so I can't show the result reliably. (ref tr-9f266766)"}
```
