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

});
