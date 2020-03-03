$( document ).ready(function() {

  // Create link and text for navigation back to the OLCF home page
  var olcf_link = document.createElement("a");
  var olcf_text = document.createTextNode("OLCF Home Page");
  olcf_link.appendChild(olcf_text);
  olcf_link.setAttribute("href", "https://olcf.ornl.gov");

  // Open OLCF home page in new tab when clicked
  olcf_link.setAttribute("target","_blank");

  var separator = document.createTextNode(" | ");

  // These items are right-aligned in the RTD theme breadcrumbs
  aside = document.querySelector("body > div > section > div > div > div:nth-child(1) > ul > li.wy-breadcrumbs-aside");

  // Next to the default "Edit on GitHub", add a separator, then the OLCF link.
  aside.appendChild(separator);
  aside.appendChild(olcf_link);

  // Insert Project Name "OLCF User Documentation" below html_logo in sidebar navigation
  var project_name_link = document.createElement("a");
  var project_name_text = document.createTextNode(" OLCF User Documentation");
  project_name_link.appendChild(project_name_text);
  project_name_link.setAttribute("href", "https://docs.olcf.ornl.gov");
  project_name_link.classList.add("icon");
  project_name_link.classList.add("icon-home");
  wysidenavsearch = document.querySelector("body > div > nav > div > div.wy-side-nav-search > a");
  wysidenavsearch.appendChild(project_name_link);


  function iconize_external_links(nav_level){
    child_list_items = nav_level.getElementsByTagName("LI");
    var i, j;
    for (i = 0; i < child_list_items.length; ++i){
      a_elements = child_list_items[i].getElementsByTagName("A");
      for (j = 0; j < a_elements.length; ++j){
        a_element = a_elements[j];
        if (a_element.getAttribute("href").includes("http")){
          var icon = document.createElement("i");
          icon.classList.add("fa");
          icon.classList.add("fa-external-link");

          var spacer = document.createTextNode(" ");
          a_element.appendChild(spacer);
          a_element.appendChild(icon);
        }
      }
    }
  }

  main_nav = document.querySelector("body > div > nav > div > div.wy-menu.wy-menu-vertical");
  training_nav = document.querySelector("body > div > nav > div > div.wy-menu.wy-menu-vertical > ul:nth-child(6) > li");
  iconize_external_links(training_nav)

});
