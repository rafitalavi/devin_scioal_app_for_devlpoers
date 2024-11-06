 // Get SEARCH FORM AND page Link
 let searchForm = document.getElementById("searchForm");
 let pageLinks = document.getElementsByClassName('page-link');

 // Ensure search form exists
 if (searchForm) {
     for (let i = 0; i < pageLinks.length; i++) {
         pageLinks[i].addEventListener('click', function (e) {
             e.preventDefault();
             // Get the data attribute
             let page = this.dataset.page;
             console.log('page:', page);
             console.log('button click');

             // Remove any existing page input to prevent duplicates
             let existingPageInput = searchForm.querySelector("input[name='page']");
             if (existingPageInput) {
                 existingPageInput.remove();
             }

             // Add hidden search input to form
             searchForm.innerHTML += `<input value="${page}" name="page" hidden />`;

             // Submit form
             searchForm.submit();
         });
     }
 }