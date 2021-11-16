console.log('HELLOOOO HI HEY')
// The user clicks on the outline heart icon to mark album as a favorite
// If the heart is solid, that means it is favorited
// If the user clicks on the solid heart, remove that album from their favorites
const csrfToken = Cookies.get('csrftoken')
const favLink = document.querySelector('.fav-link')
favLink.addEventListener('click', (event) => {
  event.preventDefault()
  const url = event.target.parentNode.href
  // check the state of whether it is favorited or not in the DOM
  const favorited = event.target.parentNode.dataset['favorited']
  const heartIcon = event.target
  const request_method = favorited === 'True' ? 'DELETE' : 'POST'
  fetch(url, {
    headers: {
      'X-Requested-With': 'XMLHttpRequest',
      'X-CSRFToken': csrfToken,
    },
    method: request_method,
  })
    .then((res) => res.json())
    .then((data) => {
      // here I can do stuff with that data!
      console.log(data)
      if (data['favorited']) {
        // replace the heart icon to solid to indicate that it IS favorited
        heartIcon.classList.replace('far', 'fas')
        // update state in the DOM to show that it is favorited
        event.target.parentNode.dataset['favorited'] = 'True'
      } else {
        // replate the heart icon class to outline to indicate that it's NOT favorited
        heartIcon.classList.replace('fas', 'far')
        // update state in the DOM to show that it is not favorited
        event.target.parentNode.dataset['favorited'] = 'False'
      }
    })
})
