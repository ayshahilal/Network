
function showForm(id) {
    document.querySelector(`#edit_form_${id}`).style.display = "block";
}
function closeForm(id) {
    document.querySelector(`#edit_form_${id}`).style.display = "none";
}

function save_post(id){
    const newPostContent = document.getElementById(`edit_content_${id}`).value;
    
    console.log(newPostContent);
    fetch(`/edit_post/${id}`, {
        method: "POST",
        body: JSON.stringify({
            new_content: newPostContent
        }),
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.getElementsByName('csrfmiddlewaretoken')[0].value
        }
    })
    .then(response => response.json())
    .then(result =>{
        console.log(result);
        document.querySelector(`#post_content_${id}`).innerHTML = result.data;
        document.querySelector(`#edit_form_${id}`).style.display = "none";
    }
        
    )
}

function delete_control(id){
    document.querySelector(`#delete_post_${id}`).style.display = "block";
}