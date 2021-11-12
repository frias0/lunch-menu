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
