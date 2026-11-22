# Run summary

| scenario | trace | query | action | outcome | http | flags |
|---|---|---|---|---|---|---|
| 01_baseline_kb | tr-10ba13e3 | How do I connect to the VPN from home? | kb | answered | - | top=vpn-setup(0.24) |
| 01_baseline_kb | tr-a06f77cc | I forgot my password, how do I reset it? | kb | answered | - | top=password-reset(0.431) |
| 01_baseline_kb | tr-69d4ad41 | How do I request access to Salesforce? | kb | answered | - | top=salesforce-access(0.561) |
| 02_baseline_tools | tr-db0a7c86 | Create a ticket: my laptop screen is flick | create_incident | ok | 201 | - |
| 02_baseline_tools | tr-2df5047e | What's the status of INC0004521? | get_incident | ok | 200 | - |
| 02_baseline_tools | tr-9398650d | Update INC0004521: user confirmed the issu | update_incident | ok | 200 | - |
| 03_vpn_answer_wrong | tr-fc4ba193 | How do I connect to the VPN from home? | kb | answered | - | top=vpn-setup-legacy(0.56); conflicting_articles; TOP_RESULT_OLDER_VERSION |
| 04_vpn_answer_retest | tr-07244bed | How do I connect to the VPN from home? | kb | answered | - | conflict_resolved; top=vpn-setup(0.229); conflicting_articles |
| 05_answers_incomplete | tr-0e2fa4dd | How do I connect to the VPN from home? | kb | answered | - | top=vpn-setup(0.374); short_chunk=12w |
| 05_answers_incomplete | tr-98e784c7 | I forgot my password, how do I reset it? | kb | answered | - | top=password-reset(0.622); short_chunk=12w |
| 05_answers_incomplete | tr-572f1eb1 | How do I request access to Salesforce? | kb | answered | - | top=salesforce-access(0.773); short_chunk=12w |
| 06_answers_retest | tr-2eb7eef8 | How do I connect to the VPN from home? | kb | answered | - | top=vpn-setup(0.24) |
| 06_answers_retest | tr-0f4ee70c | I forgot my password, how do I reset it? | kb | answered | - | top=password-reset(0.431) |
| 06_answers_retest | tr-e7fbd9d9 | How do I request access to Salesforce? | kb | answered | - | top=salesforce-access(0.561) |
| 07_tickets_all_failing | tr-9c11c567 | Create a ticket: my laptop screen is flick | create_incident | auth_failed | 401 | - |
| 07_tickets_all_failing | tr-cdfe7d71 | What's the status of INC0004521? | get_incident | auth_failed | 401 | - |
| 08_tickets_intermittent | tr-667d852a | What's the status of INC0004521? | get_incident | ok | 429,429,200 | retry; retry |
| 09_tickets_busy_all_day | tr-ecfbb7a3 | What's the status of INC0004521? | get_incident | rate_limited | 429,429,429 | retry; retry |
| 10_ticket_not_found | tr-58a27228 | What's the status of ticket 4521? | get_incident | not_found | 404 | - |
| 11_not_found_retest | tr-2346f4b1 | What's the status of ticket 4521? | get_incident | ok | 200 | arg_normalized(4521->INC0004521) |
| 12_after_api_upgrade | tr-cc22bc61 | Create a ticket: my laptop screen is flick | create_incident | bad_request | 422 | - |
| 12_after_api_upgrade | tr-9f266766 | What's the status of INC0004521? | get_incident | schema_mismatch | 200 | schema_mismatch(missing=short_description,state) |
