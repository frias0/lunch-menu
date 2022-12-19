window.onload = (event) => {
   var wrongDate = new Date(Date.parse(/(\d\d\d\d-\d\d-\d\d)/.exec(document.querySelector(".updated").textContent)[0]))
   var wrongDateUTC = new Date(wrongDate.toLocaleString("sv-SE",{timeZone: "UTC"}))
   var wrongDateLocal = new Date(wrongDate.toLocaleString("sv-SE",{timeZone: "Europe/Stockholm"}))
   var offset = wrongDateUTC.getTime()-wrongDateLocal.getTime()
   var lastUpdate = new Date(wrongDate.getTime() + offset)
   if(new Date().getDate() > lastUpdate.getDate()){
      console.log("NOT UPDATED")
      document.querySelector("#content").classList.add("stale")
      document.querySelector(".warning").style.display="block"
   }
}

function copyToClipboard() {

   var doc = document
   , text = doc.getElementById("content")
   , range, selection;

if (doc.body.createTextRange)
{
   range = doc.body.createTextRange();
   range.moveToElementText(text);
   range.select();
} 

else if (window.getSelection)
{
   selection = window.getSelection();        
   range = doc.createRange();
   range.selectNodeContents(text);
   selection.removeAllRanges();
   selection.addRange(range);
}
document.execCommand('copy');
window.getSelection().removeAllRanges();
document.getElementById("copy_button").text="Copied";
}