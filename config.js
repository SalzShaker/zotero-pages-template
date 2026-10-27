// ------------------------------------------------------------------
//  Edit this file – nothing else is needed to get started.
// ------------------------------------------------------------------
const CONFIG = {
  // Page title and the text below it
  title: "My DH bibliography",
  intro: "An annotated bibliography on … Built from my Zotero library via the Zotero API.",

  // Which library?
  //   group library:  libraryType "groups", libraryId = number in zotero.org/groups/<number>/…
  //   own library:    libraryType "users",  libraryId = your userID (zotero.org/settings/keys)
  //                   – your library must be public: zotero.org/settings/privacy → «Publish Entire Library»
  libraryType: "users",
  libraryId: "21774691",          // dh_unibe (open group of DH Bern)

  // Where the page gets the data:
  //   "api"  – the browser asks the Zotero API on every visit (public libraries only, no key)
  //   "file" – the page reads data/items.json, written by the GitHub Action with your secret key
  //            (private libraries; see README → «Private library»)
  source: "api",


  // Citation style (any CSL style id, e.g. "apa", "chicago-author-date", "modern-language-association")
  style: "chicago-author-date",

  // Group the list: "none", "year", "type" or "tag"
  groupBy: "year",

  // Show child notes from Zotero below each entry (your annotations!)
  showNotes: true,

  // Safety net: stop after this many items (the API sends 100 per request)
  maxItems: 500
};
// NEVER put an API key in this file – everything here is public.
