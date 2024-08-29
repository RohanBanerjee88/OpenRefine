// Right now we do not need the extensive use of form.js, it's a basic example that includes form validation and possibly hiding/showing advanced options if needed.


'use strict';

/**
 * Hide an option by form_id
 *
 * @param      {string}  form_id  The form identifier
 */
function hide_option(form_id) {
  let form_element = $(form_id);
  let parent = form_element.parent();
  parent.hide();
}

/**
 * Show an option by form_id
 *
 * @param      {string}  form_id  The form identifier
 */
function show_option(form_id) {
  let form_element = $(form_id);
  let parent = form_element.parent();
  parent.show();
}

/**
 * Clamp between two numbers
 *
 * @param      {number}  min     The minimum
 * @param      {number}  max     The maximum
 * @param      {number}  val     The value to clamp
 */
function clamp(min, max, val) {
  return Math.min(max, Math.max(min, val));
}

/**
 * Register event handlers and initial logic on document ready
 */
$(document).ready(function() {
  // Example: Validate memory input field
  $('#batch_connect_session_context_memory').change(function() {
    let memory_input = $(this).val();
    if (!memory_input.match(/[0-9]+([gmtGMT][bB])?/)) {
      alert("Invalid memory format. Please enter a value like '100GB' or '500MB'.");
      $(this).val('');  // Reset the input field
    }
  });

  // Example: Show/hide advanced options based on a checkbox
  $('#batch_connect_session_context_advanced_options').change(function() {
    if ($(this).is(':checked')) {
      show_option('#batch_connect_session_context_node_type');
      show_option('#batch_connect_session_context_num_gpus');
    } else {
      hide_option('#batch_connect_session_context_node_type');
      hide_option('#batch_connect_session_context_num_gpus');
    }
  });
});
