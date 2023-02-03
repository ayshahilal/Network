

function like_post(id){
    document.getElementById(`like_${id}`).style.display = "none";
   
   fetch(`/like/${id}`)
   .then(response => response.json())
   .then(result => {
       document.getElementById(`unlike_${id}`).style.display = "block";
       
       document.getElementById(`howmanylikes_${id}`).innerHTML = `${result.data}`;
       
       console.log(result.data);
   });
}

function unlike_post(id){
   document.getElementById(`unlike_${id}`).style.display = "none";
   
   fetch(`/unlike/${id}`)
   .then(response => response.json())
   .then(result => {
       document.getElementById(`like_${id}`).style.display = "block";

       document.getElementById(`howmanylikes_${id}`).innerHTML = `${result.data}`;
      
       console.log(result.data);
   });
}