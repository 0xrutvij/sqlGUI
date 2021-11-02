# Application Quickstart Guide

<hr/>

### Home Page

- On app launch, the user views this page which consists a listing of all the contacts within the contact list.
- Browse LR-TD to view details of a contact and more contacts
- Select a single contact row and press `Delete` or `Edit` to make changes to the listing.
- Press `Add` to pull up a new contact form & add a new contact.

### New Contact Form + Contact Edit Form

- Both these views are similar, in the case of latter the current contacts' properties are populated within the form
and can be edited further.
- Shows the full name, list of addresses, list of phones & a list of
dates for a user. Any of these can be selected and edited using their
respective interfaces. 
- This view also allows for the addition of new addresses, phones and dates
for a given user.
- Sub-views are intuitive, in that they're text-fields and can be edited to the value desired.
Note: There is no input validation in this version of the appication & thus it is on the user
to ensure the input is correct.
- Saving a sub-view confirms changes to properties & cancel rejects any changes.
- Saving the form confirms all changes & returns to home page.

### Search Page

- Using the tab navigation on the home page, user can switcht to the search page.
- For the search box, search is triggered as the user types & continuously refreshes as long
as matches are found.
- Boolean search is possible, `,` represents the `OR` operation and
`;` represents the `AND` operation.
- Double-quoted strings can be used for exact matches.
- Examples of search-strings
  - ```text
    <name>; <state>; <date_type>
    ```
  - ```text
    <name>, <name>; <state>
    ```
- Results with partial match are also listed when possible due to the use of
`trigram` tokenizer.
- Spaces between words act like implicit `AND` operations.
- Results displayed on search can be selected one at a time to `Edit` or `Delete`.
- Editing a result launches the Contact Edit Form. 