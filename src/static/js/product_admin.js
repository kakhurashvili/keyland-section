(function($) {
    $(document).ready(function() {
      var categorySelect = $('.category-select');
      var subcategorySelect = $('.subcategory-select');
  
      // Function to populate the subcategory options based on the selected category
      function populateSubcategories() {
        var selectedCategoryId = categorySelect.val();
        var subcategoryUrl = '/get_subcategories/?category_id=' + selectedCategoryId;
  
        subcategorySelect.empty(); // Clear existing options
  
        // Retrieve the subcategories using an AJAX request
        $.getJSON(subcategoryUrl, function(data) {
          $.each(data, function(key, value) {
            subcategorySelect.append('<option value="' + value.id + '">' + value.title + '</option>');
          });
        });
      }
  
      // Event handler for category selection change
      categorySelect.on('change', function() {
        populateSubcategories();
      });
  
      // Initial population of subcategories on page load
      populateSubcategories();
    });
  })(django.jQuery);
  