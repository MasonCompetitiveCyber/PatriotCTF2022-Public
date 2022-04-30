var pages = {
  home: "Welcome to my completely unhackable site. There are no flags here, so don\'t even bother trying to look for them lol.",
  about: "This site is 100% completely utterly unhackable, and anyone who says anything otherwise is an idiot who knows nothing about cybersecurity.",
  contact: "Do you want to get the flag? If you do, then contact me at hahahahah.jk.im.not.giving.you.the.flag@lol.com."
};

function getContent(fragmentId, callback){
  callback(pages[fragmentId]);
}

function loadContent(){
  var contentDiv = document.getElementById("app"),
      fragmentId = location.hash.substr(1);

  getContent(fragmentId, function (content) {
    contentDiv.innerHTML = content;
  });
}

var thing = atob(atob(atob("VERKR2EySlhiSFZNTUVaTVUydFNWRk5yV2t4U1JrNUxWRVZHVkZKcE9YSmpNbmhyWVcxYWRtRlhSbXRqTWxsMVpFaG9NQT09")));

fetch(thing).then(function(response) {
  return response.text();
}).then(function(data) {
  pages["secret"] = data;

  if(!location.hash) {
    location.hash = "#home";
  }
  loadContent();

  window.addEventListener("hashchange", loadContent)
});
