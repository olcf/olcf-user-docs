$( document ).ready(function() {

  // Create link and text for navigation back to the OLCF home page
  var olcf_link = document.createElement("a");
  var olcf_text = document.createTextNode("OLCF Home Page");
  olcf_link.appendChild(olcf_text);
  olcf_link.setAttribute("href", "https://olcf.ornl.gov");

  // Open OLCF home page in new tab when clicked
  olcf_link.setAttribute("target","_blank");

  // Create link and text for navigation back to the myOLCF home page
  var myolcf_link = document.createElement("a");
  var myolcf_text = document.createTextNode("myOLCF");
  myolcf_link.appendChild(myolcf_text);
  myolcf_link.setAttribute("href", "https://my.olcf.ornl.gov");

  // Open myOLCF home page in new tab when clicked
  myolcf_link.setAttribute("target","_blank");

  var separator = document.createTextNode(" | ");

  // These items are right-aligned in the RTD theme breadcrumbs
  aside = document.querySelector("body > div > section > div > div > div:nth-child(1) > ul > li.wy-breadcrumbs-aside");

  // Next to the default "Edit on GitHub", add a separator, then the OLCF links.
  aside.appendChild(separator);
  aside.appendChild(olcf_link);
  aside.appendChild(separator.cloneNode(true)) // have to append a copy
  aside.appendChild(myolcf_link);

  // Insert "Help email" below html_logo in sidebar navigation
  var help_link = document.createElement("a");
  var help_link_text = document.createTextNode("Need Help? Contact us. ");
  var email_link_text = document.createTextNode(" help@olcf.ornl.gov");
  help_link.appendChild(help_link_text);
  help_link.appendChild(email_link_text);
  help_link.setAttribute("href","https://docs.olcf.ornl.gov/support/index.html");
  
  wysidenavsearch = document.querySelector("body > div > nav > div > div.wy-side-nav-search > a");
  wysidenavsearch.appendChild(help_link);

  // For any external links in the main navigation, append the FontAwesome external link icon.
  function iconize_external_links(nav_level){
    a_elements = nav_level.getElementsByTagName("A");
    for (var i = 0; i < a_elements.length; ++i){
      if (a_elements[i].getAttribute("href").includes("http")){
         var icon = document.createElement("i");
         icon.classList.add("fa");
         icon.classList.add("fa-external-link");
         var spacer = document.createTextNode(" ");
         a_elements[i].appendChild(spacer);
         a_elements[i].appendChild(icon);
      }
    }
  }

  iconize_external_links(document.querySelector("body > div > nav > div > div.wy-menu.wy-menu-vertical"))

});
