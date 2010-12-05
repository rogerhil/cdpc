/* Copyright (C) 2010  Marcos Lopes <marcosmlopes01@gmail.com>
 * Copyright (C) 2010  Rogério Hilbert Lima <rogerhil@gmail.com>
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Affero General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

$(function() {
    if(!supports_placeholder()) {
        $('*[placeholder]').each(function() {
            var placeholder = $(this).attr('placeholder');
            if($(this).val() == '') $(this).val(placeholder);
        });
        $('*[placeholder]').resetDefaultValue();
        $('*[placeholder]').parents('form').bind('submit', function() {
            $('*[placeholder]', $(this)).each(function() {
                if($(this).val() == $(this).attr('placeholder')) {
                    $(this).val('');
                }
            });
        });
    }
});

function supports_placeholder() {
    var input = document.createElement('input');
    if('placeholder' in input) return true;
    return false;
}

/**
 * jQuery resetDefaultValue plugin
 * @version 0.9.1
 * @author Leandro Vieira Pinho 
 */
jQuery.fn.resetDefaultValue = function() {
    function _clearDefaultValue() {
        var _$ = $(this);
        if ( _$.val() == _$.attr('placeholder') ) {
            _$.val('');
    	    _$.removeClass('disabled');
        }
    }
    function _resetDefaultValue() {
        var _$ = $(this);
        if ( _$.val() == '' ) {
            _$.val(_$.attr('placeholder'));
	        _$.addClass('disabled');
        }
    }
    return this.click(_clearDefaultValue)
               .focus(_clearDefaultValue)
               .blur(_resetDefaultValue);
}

