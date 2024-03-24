const ID_RE = /(-)_(-)/;

/**
 * Replace the template index of an element (-_-) with the
 * given index.
 */
function replaceTemplateIndex(value, index) {
    return value.replace(ID_RE, '$1' + index + '$2');
}

/**
 * Adjust the indices of form fields when removing items.
 */
function adjustIndicesIngredients(removedIndex) {
    var $forms = $('.ingredients-subform');

    $forms.each(function () {
        var $form = $(this);
        var index = parseInt($form.attr('data-index'));
        var newIndex = index - 1;

        // Update data-index for all elements with an index greater than the removed index
        if (index > removedIndex) {
            var newFormIndex = newIndex;
            var newIndexAttr = newIndex;
            var regex = new RegExp('(-)' + index + '(-)');
            var repVal = '$1' + newIndex + '$2';

            // Update ID in form itself
            $form.attr('id', $form.attr('id').replace(index, newIndexAttr));
            $form.data('index', newFormIndex);

            // Update IDs in form fields
            $form.find('label').each(function () {
                var $item = $(this);
                $item.attr('for', $item.attr('for').replace(index, newIndexAttr));
            });

            $form.find('input').each(function () {
                var $item = $(this);
                $item.attr('id', $item.attr('id').replace(index, newIndexAttr));
                $item.attr('name', $item.attr('name').replace(index, newIndexAttr));
            });

            // Update data-index attribute
            $form.attr('data-index', newFormIndex);
        }
    });
}

/**
 * Remove a form.
 */
function removeIngredientForm() {
    event.preventDefault();

    var $removedForm = $(this).closest('.ingredients-subform');
    var removedIndex = parseInt($removedForm.attr('data-index'));
    $removedForm.remove();

    // Update indices
    adjustIndicesIngredients(removedIndex);
}

/**
 * Add a new form.
 */
function addIngredientsForm() {
    event.preventDefault();

    var $templateForm = $('#ingredients-_-form');

    if ($templateForm.length === 0) {
        console.log('[ERROR] Cannot find template');
        return;
    }

    // Get Last index
    var $lastForm = $('.ingredients-subform').last();

    var newIndex = 0;

    if ($lastForm.length > 0) {
        newIndex = parseInt($lastForm.attr('data-index')) + 1;
    }

    // Maximum of 20 subforms
    if (newIndex >= 60) {
        console.log('[WARNING] Reached maximum number of elements');
        return;
    }

    // Add elements
    var $newForm = $templateForm.clone();

    $newForm.attr('id', replaceTemplateIndex($newForm.attr('id'), newIndex));

    $newForm.attr('data-index', newIndex);

    $newForm.find('label').each(function () {
        var $item = $(this);
        $item.attr('for', replaceTemplateIndex($item.attr('for'), newIndex));
    });

    $newForm.find('input').each(function () {
        var $item = $(this);
        $item.attr('id', replaceTemplateIndex($item.attr('id'), newIndex));
        $item.attr('name', replaceTemplateIndex($item.attr('name'), newIndex));
    });

    // Append
    $('#subforms-container-ingredients').append($newForm);
    $newForm.addClass('ingredients-subform');
    $newForm.removeClass('is-hidden');

    $newForm.find('.remove-ingredient-item').click(removeIngredientForm);
}


/**
 * Adjust the indices of form fields when removing items.
 */
function adjustIndicesSteps(removedIndex) {
    var $forms = $('.steps-subform');

    $forms.each(function () {
        var $form = $(this);
        var index = parseInt($form.attr('data-index'));
        var newIndex = index - 1;

        // Update data-index for all elements with an index greater than the removed index
        if (index > removedIndex) {
            var newFormIndex = newIndex;
            var newIndexAttr = newIndex;
            var regex = new RegExp('(-)' + index + '(-)');
            var repVal = '$1' + newIndex + '$2';

            // Update ID in form itself
            $form.attr('id', $form.attr('id').replace(index, newIndexAttr));
            $form.data('index', newFormIndex);

            // Update IDs in form fields
            $form.find('label').each(function () {
                var $item = $(this);
                $item.attr('for', $item.attr('for').replace(index, newIndexAttr));
            });

            $form.find('textarea').each(function () {
                var $item = $(this);
                $item.attr('id', $item.attr('id').replace(index, newIndexAttr));
                $item.attr('name', $item.attr('name').replace(index, newIndexAttr));
            });

            // Update data-index attribute
            $form.attr('data-index', newFormIndex);
        }
    });
}

/**
 * Remove a form.
 */
function removeStepForm() {
    event.preventDefault();

    var $removedForm = $(this).closest('.steps-subform');
    var removedIndex = parseInt($removedForm.attr('data-index'));
    $removedForm.remove();

    // Update indices
    adjustIndicesSteps(removedIndex);
}

/**
 * Add a new form.
 */
function addStepsForm() {
    event.preventDefault();

    var $templateForm = $('#steps-_-form');

    if ($templateForm.length === 0) {
        console.log('[ERROR] Cannot find template');
        return;
    }

    // Get Last index
    var $lastForm = $('.steps-subform').last();

    var newIndex = 0;

    if ($lastForm.length > 0) {
        newIndex = parseInt($lastForm.attr('data-index')) + 1;
    }

    // Maximum of 20 subforms
    if (newIndex >= 60) {
        console.log('[WARNING] Reached maximum number of elements');
        return;
    }

    // Add elements
    var $newForm = $templateForm.clone();

    $newForm.attr('id', replaceTemplateIndex($newForm.attr('id'), newIndex));

    $newForm.attr('data-index', newIndex);

    $newForm.find('label').each(function () {
        var $item = $(this);
        $item.attr('for', replaceTemplateIndex($item.attr('for'), newIndex));
    });

    $newForm.find('textarea').each(function () {
        var $item = $(this);
        $item.attr('id', replaceTemplateIndex($item.attr('id'), newIndex));
        $item.attr('name', replaceTemplateIndex($item.attr('name'), newIndex));
    });

    // Append
    $('#subforms-container-steps').append($newForm);
    $newForm.addClass('steps-subform');
    $newForm.removeClass('is-hidden');

    $newForm.find('.remove-step-item').click(removeStepForm);
}

$(document).ready(function () {
    $('.add-new-ingredient').click(addIngredientsForm);
    $('.remove-ingredient-item').click(removeIngredientForm);

    $('.add-new-step').click(addStepsForm);
    $('.remove-step-item').click(removeStepForm);
    
    document.addEventListener('DOMContentLoaded', function() {
        let pageTitle = document.querySelector('title').getAttribute('title');
        document.title = pageTitle;
    });
});

