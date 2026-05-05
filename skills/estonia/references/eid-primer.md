# Estonian eID — Smart-ID, Mobile-ID, ID-card

Most Estonian government transactions require authenticating with one of three electronic identity tools. A skill in this repository will walk a user up to the point of authentication and then hand off — skills do not impersonate users or transact on their behalf.

## Smart-ID
A mobile-app-based authentication and signing tool issued by SK ID Solutions. Available to citizens and residents of Estonia, Latvia, and Lithuania. Free for personal use. Works without a SIM card. https://www.smart-id.com

## Mobile-ID
A SIM-based authentication tool — the user's phone number itself becomes their digital ID. Requires support from the user's mobile operator. Estonian only. Issued via the operator + Politsei- ja Piirivalveamet (PPA).

## ID-card
The physical Estonian ID-card with an embedded chip. Requires a card reader connected to the user's computer. The legal default; every Estonian citizen and most residents have one. https://www.id.ee

## e-Residency card
A subset of the ID-card capability issued to non-residents who have applied for and received e-Residency. Allows e-Residents to authenticate to Estonian e-services and digitally sign documents, but does **not** confer residence, citizenship, or tax residency. https://www.e-resident.gov.ee

## When a skill says "log in with your eID"
The user picks whichever of the four they have available. Most government portals accept all four (or all three, depending on the user's residency status). Skills should phrase this as "log in with your Smart-ID, Mobile-ID, or ID-card" and let the user choose.
