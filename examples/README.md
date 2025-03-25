Run here the workflow server manager cli `wfsm` v0.0.1:
```bash
./wfsm deploy -m ./marketing-campaign/deploy/marketing-campaign.json -e ./marketing-campaign/deploy/marketing_campaign_example.yaml

[...]

[+] Running 1/1
 ✔ Container orgagntcymarketing-campaign-org.agntcy.marketing-campaign-1  Started                                                                                                                                 0.5s 
2025-03-25T18:15:50+01:00 INF ---------------------------------------------------------------------
2025-03-25T18:15:50+01:00 INF agent running in container: org.agntcy.marketing-campaign, listening on: http://127.0.0.1:56338
2025-03-25T18:15:50+01:00 INF API Key: b7d56a0e-ef93-4039-9b15-9956d9c10b51
2025-03-25T18:15:50+01:00 INF ---------------------------------------------------------------------

[...]
2025-03-25T18:15:50+01:00 INF agent_workflow_server.agents.load Registered Agent: '6c99c2fb-90a4-47cb-a3f2-8608f3959b9c'
```

Once started, get the api send:

```bash
curl --location 'http://localhost:56058/runs' \
--header 'Content-Type: application/json' \
--header 'Accept: application/json' \
--header 'x-api-key: 922ff044-8227-4e9e-ada4-79f4bfffdcfb' \
--data-raw '{
    "agent_id": "6c99c2fb-90a4-47cb-a3f2-8608f3959b9c",
    "thread_id": "1",
    "input": {
        "messages": [
{"type":"human","content":"**************\n\nSubject: March Green Sale\n\nDear [Client'\''s Name],\n\nI hope this message finds you well. We are excited to announce an exclusive offer from our brand, Verdant Vogue, that you won'\''t want to miss!\n\nThis March, we'\''re celebrating the vibrant spirit of spring with a special 20% discount on all our green clothing items. Whether you'\''re looking to refresh your wardrobe with the latest trends or add a pop of color to your style, our collection has something for everyone.\n\nExplore our range of eco-friendly and fashion-forward designs, crafted with the finest materials to ensure both comfort and style. This limited-time offer is our way of saying thank you for being a valued part of the Verdant Vogue community.\n\nVisit our website or your nearest store to take advantage of this exclusive discount. Don'\''t miss out—this offer is valid only until the end of March!\n\nThank you for choosing Verdant Vogue. We look forward to seeing you embrace the green this season.\n\nWarm regards,\n\n[Your Full Name]  \n[Your Position]  \nVerdant Vogue  \n[Contact Information]\n**************"},
            {
                "content": "OK",
                "type": "human"
            }
        ]
    },
    "metadata": {},
    "config": {
        "recipient_email_address": "Name Surname <your@domain.com>",
        "sender_email_address": "test@demo.com",
        "target_audience": "academic"
    }
}

'
```