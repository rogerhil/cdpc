/* Copyright (C) 2010  Rogerio Hilbert Lima <rogerhil@gmail.com>
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

function showLoginForm(msg, callback) {
    $("#ajax_login").dialog({buttons: [
        {text: "Fechar",
         click: function () {$(this).dialog("close");}},
        {text: "Autenticar",
         click: function () { doLogin(callback); }}
    ], modal: true});
    $("#description_message").html(msg);
}

function doLogin(callback) {
    var $email = $('input[name=email]', '#form_ajax_login');
    var email = $email.val();
    var password = $('input[name=senha]', '#form_ajax_login').val();
    var url = '/ajax_login';
    var $errorBlock;
    
    var writeError = function (msg) {
        $errorBlock = $('#login_error');
        if (!$errorBlock.length) {
            $errorBlock = $('<div class="site-message error" id="login_error">' + msg + '</div>');
            $errorBlock.insertBefore($email.parent());
        } else {
            $errorBlock.html(msg);
        }
        $errorBlock.effect('bounce', {times: 3, direction: 'down', distance: 20}, 200);
    }
    
    if (!email.length && !password.length) {
        writeError("Campos obrigatórios.");
        return;   
    }

    var data = {email: email, password: password};

    var success = function (data) {
        if (data.success) {
            $errorBlock = $('#login_error');
            $errorBlock.remove();
            $("#ajax_login").dialog('close');
            if (callback) {
                callback();
            }
        } else {
            writeError(data.message);
        }
    }
    $.post(url, data, success, 'json');
}

function testIsAuthenticated(callbackSuccess, callbackFailed) {
    var url = '/ajax_is_logged_in';
    var success = function (data) {
        if (data.authenticated) {
            callbackSuccess();
        } else {
            callbackFailed();
        }
    }
    $.getJSON(url, {}, success);
}
