/* Copyright (C) 2010  Lincoln de Sousa <lincoln@comum.org>
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


String.prototype.capitalize = function(){
    return this.replace(/(^|\s)([a-z])/g,
                        function(m,p1,p2){return p1+p2.toUpperCase();});
};

var load = function () {
    if (this.checked || this.selected) $(this).change();
};

var VALIDATOR, CURRENT_STEP;

function carregar () {
    // Javascript da pagina Cadastro de projetos
    if ($('body.project_register').length == 0) return;

    CURRENT_STEP = $('input[name=step]').val();
    
    var rules = {parcerias: {atLeastOne: true},
                 acao_cultura_viva: {atLeastOne: true},
                 atividade: {atLeastOne: true}};
    
    VALIDATOR = $('#content form').validate({rules: rules, debug: true});
    configFields();

    var prev = $('<a href="#">').addClass('previous').text('Voltar');
    var nex = $('<a href="#">').addClass('next').text('Próximo');
    var buttons = $('<div class="buttons">').append(nex);
    $('div.step').hide()
    $('div.step:not(#project_index) div.main').append(buttons);
    $('div.step:not(#project_data) div.buttons').prepend(prev);
    $('div#' + CURRENT_STEP).show();
    $('ul.steps li.active').removeClass('active');
    $('ul.steps li.' + CURRENT_STEP).addClass('active');

    $('div.step div.buttons .next').click(next);
    $('div.step div.buttons .previous').click(previous);
}

function configFields() {
    supportsPlaceholder();
    $('input.cep').mask('99.999-999');
    $('input.phone').mask('(99) 9999-9999');
}

function validateStep() {
    var valid = true;
    var selector = "div#" + CURRENT_STEP + " input, " +
                   "div#" + CURRENT_STEP + " select, " +
                   "div#" + CURRENT_STEP + " textarea"
    $(selector).each(function () {
        var ret = false;
        // Não validar campos que estão escondidos
        $(this).parents().each(function () {
            if ($(this).is(':hidden')) ret = true;
        });
        if (ret) return;
        if (VALIDATOR.element($(this)) == false) valid = false;
    });
    return valid;
}

function next(e) {
    var next_step = $('div#' + CURRENT_STEP).next().attr('id');
    var valid = validateStep();
    alert(VALIDATOR.numberOfInvalids());
    if (valid) {
        $('div#' + CURRENT_STEP).fadeOut('fast', function() {
            $('div#' + next_step).fadeIn('fast');
            $('ul.steps li.active').removeClass('active');
            $('ul.steps li.' + next_step).addClass('active');
            $('input[name=step]').val(next_step);
            CURRENT_STEP = next_step;
            clicked = 0;
        });
    } else {
        $('html, body').animate({scrollTop: 0}, 'slow');
    }
    
    e.preventDefault();
}

function previous(e) {
    var previous_step = $('div#' + CURRENT_STEP).prev().attr('id');
    $('div#' + CURRENT_STEP).fadeOut('fast', function() {
        $('div#' + previous_step).fadeIn('fast');
        $('ul.steps li.active').removeClass('active');
        $('ul.steps li.' + previous_step).addClass('active');
        $('input[name=step]').val(previous_step);
        CURRENT_STEP = previous_step;
    });
    e.preventDefault();
}

function loadDadosProjeto() {
    $("input[name=participa_cultura_viva]").change(function () {
        loadRadioMultipleExtra(this, 'sim', 'participa_cultura_viva_sim');
    });

    $("input[name=estabeleceu_parcerias]").change(function () {
        loadRadioMultipleExtra(this, 'sim', 'parcerias_sim');
    });
    
    loadRadioMultipleExtra($("input[name=participa_cultura_viva]:checked"),
                           'sim', 'participa_cultura_viva_sim');
    loadRadioMultipleExtra($("input[name=estabeleceu_parcerias]:checked"),
                           'sim', 'parcerias_sim');

}

function loadLocalizacaoGeoProjeto() {
    $('#local_proj').change(function () {
        var li = $(this).parents("li")[0];
        if ($(this).val () == 'outros') {
            $('#local_proj_outros').show ();
            $('#local_proj_outros_novo').show ();
            $(li).addClass("subhead");
        } else {
            $('#local_proj_outros').hide ();
            $('#local_proj_outros_novo').hide ();
            $(li).removeClass("subhead");
        }
    });
    $('#local_proj').change();
}

function loadComunicacaoCulturaDigital() {
    $("input[name=sede_possui_tel]").change(function () {
        loadRadioSingleExtra(this, 'sim', 'sede_possui_tel_sim', 'sede_possui_tel_nao');
    });

    $("input[name=sede_possui_net]").change(function () {
        loadRadioSingleExtra(this, 'sim', 'sede_possui_net_sim', 'sede_possui_net_nao');
    });
    
    $('#pq_sem_tel').change(function () {
        if ($(this).val () == 'outro') {
            $('#pq_sem_tel_outro_escolhido').show ();
        } else {
            $('#pq_sem_tel_outro_escolhido').hide ();
        }
    });

    $('#pq_sem_internet').change(function () {
        
        if ($(this).val () == 'outro') {
            $('#pq_sem_internet_outro_escolhido').show ();
        } else {
            $('#pq_sem_internet_outro_escolhido').hide ();
        }
    });

    loadRadioSingleExtra($("input[name=sede_possui_tel]:checked"),
                         'sim', 'sede_possui_tel_sim', 'sede_possui_tel_nao');
    loadRadioSingleExtra($("input[name=sede_possui_net]:checked"),
                         'sim', 'sede_possui_net_sim', 'sede_possui_net_nao');
    
    var change = function (id) {
        if ($('#' + id).val () == 'outro') {
            $('#' + id + '_outro_escolhido').show ();
        } else {
            $('#' + id + '_outro_escolhido').hide ();
        }
    
    }
    change('pq_sem_tel');
    change('pq_sem_internet');

}

function loadEntidadeProponente() {
    $("input[name=convenio_ent]").change(function () {
        loadRadioSingleExtra(this, 'sim', 'convenio_ent_sim');
    });

    $("input[name=endereco_ent_proj]").change(function () {
        loadRadioMultipleExtra(this, 'nao', 'endereco_ent_proj_nao');
    });
    loadRadioSingleExtra($("input[name=convenio_ent]:checked"), 'sim', 'convenio_ent_sim');
    loadRadioMultipleExtra($("input[name=endereco_ent_proj]:checked"), 'nao', 'endereco_ent_proj_nao');
}

function loadParceriasProjeto() {

}

function loadAtividadesExercidasProjeto() {

}

$(document).ready (function () {

    loadDadosProjeto();
    loadLocalizacaoGeoProjeto();
    loadComunicacaoCulturaDigital();
    loadEntidadeProponente();
    loadParceriasProjeto();
    loadAtividadesExercidasProjeto();

    $('input[name=outras_atividades]').change(function () {
        if ($(this).is (':checked')) {
            $('#outras_atividades_escolhido').show ();
        } else {
            $('#outras_atividades_escolhido').hide ();
        }
    });

    $('input[name=outras_culturas]').change(function () {
        if ($(this).is (':checked')) {
            $('#outras_culturas_escolhido').show ();
        } else {
            $('#outras_culturas_escolhido').hide ();
        }
    });

    $('input[name=outra_ocupacao]').change(function () {
        if ($(this).is (':checked')) {
            $('#outra_ocupacao_escolhido').show ();
        } else {
            $('#outra_ocupacao_escolhido').hide ();
        }
    });

    $('input[name=outras_manifestacoes]').change(function () {
        if ($(this).is (':checked')) {
            $('#outras_manifestacoes_escolhido').show ();
        } else {
            $('#outras_manifestacoes_escolhido').hide ();
        }
    });
    
    carregar();
});

function novoEndereco () {
    var $newElement = $($('#local_proj_outros')[0].children[0].cloneNode (true));
    $('input, select', $newElement).val ('');
    $('.error-message', $newElement).remove();
    $('.error', $newElement).removeClass('error');

    var $remove = $('<a href="javascript:;">Remover endereço</a>');
    var title = $('<a>Outro endereço</a>');
    title.css('padding', '0px');
    title.css('margin', '0px');
    $newElement.css('margin', '20px 0px 0px 0px');
    $remove.click (function (evt) {
        $newElement.parent().remove ();
    });

    $newElement.removeClass ('subbody');
    $newElement.removeAttr('id');
    $('<div class="subadded">')
        .append (title)
        .append ($newElement)
        .appendTo ($('#local_proj_outros'));
    $('<div style="text-align: right;">')
        .append($remove)
        .appendTo ($newElement.parent());
    atualizarEnderecos ();
}

function atualizarEnderecos () {
    var $select = $('select[name=local_projeto]');
    var selected = $select.val ();
    $('option', $select).each (function () {
        if ($(this).val () != '' &&
            $(this).val () != 'itinerante') {
            $(this).remove();
        }
    });
    $('div.formEndereco').each (function () {
        var $div = $(this);
        var nome = $('input[name=end_nome]', $div).val ();
        if (nome != '') {
            var $opt = $('<option>')
                .appendTo($select);
            $opt.val(nome);
            $opt.attr('value', nome)
            $opt.html(nome)
            if (nome == selected)
                $opt.attr('selected', 'selected');
        }
    });
}

function novaDocumentacao ($parent) {
    var $remove = $('<a href="javascript:;">Remover</a>');
    $remove.click (function (evt) {
        $(this).parent().remove();
    });

    var $label = $('<label>' +
        'Upload de <b>Plano de trabalho e documentações do Projeto</b>' +
        '<input type="file" name="documentacoes"/>' +
        '</label>');
    $('<li>')
        .append ($label)
        .append ($remove)
        .addClass ('bottomBorder')
        .appendTo ($parent);
}

function novoConvenio ($parent) {
    var $remove = $('<a href="javascript:;">Remover</a>');
    $remove.click (function (evt) {
        $(this).parent().remove();
    });

    var $label = $('<input type="text" name="outro_convenio" ' + 
                   'class="textarea" />');

    $('<li class="extra">')
        .append ($label)
        .append ($remove)
        .appendTo ($parent);
    
}

function novoParceiro ($parent) {
    var $remove = $('<a href="javascript:;" style="float: right;">Remover</a>');
    $remove.click (function (evt) {
        $(this).parent().remove();
    });

    var $label = $('<label>' +
        '<input type="text" name="parcerias" class="required textarea large" />' +
        '</label>');
    $('<li>')
        .append ($label)
        .append ($remove)
        .addClass ('bottomBorder')
        .appendTo ($parent);
}

function preencherCamposLista(values, errors) {
    var thee, thev;

    for (var key in values) {
        thev = values[key];
        $('input[name=' + key + ']').each(function () {
            $(this).val(thev.splice(0,1));
        });
    }

    for (var key in errors) {
        $('input[name=' + key + ']').each(function () {
            thee = errors[key].splice(0,1);
            if (thee != '') {
                $(this).addClass("error");
                $('<div class="error-message">' + thee + '</div>').insertAfter($(this));
            }
        });
    }
}

function novosCamposLista(values) {
    var funcs = {'rs_nome': novaEntrada,
                 'feed_nome': novaEntrada,
                 'proj_tel': novoTelefone,
                 'ent_tel': novoTelefone,
                 'end_outro_bairro': novoEndereco};
    var blocksSet = {'rs_nome': $('#redesSociais'),
                     'feed_nome': $('#feeds'),
                     'proj_tel': $('#proj_tel'),
                     'ent_tel': $('#ent_tel'),
                     'end_proj_complemento': $('#localizacaoGeoProjetoSection')};
    var items;
    for (var id in values) {
        items = values[id];
        for (var k = 0; k < items.length; k++) {
            if (k < 1) continue;
            if (funcs[id]) {
                funcs[id](blocksSet[id], id.split('_')[0]);
            }
        }
    }
}

function proximo() {
    var current = $("#"+currentTab);
    var next = current.next();
    var children = current.children();
    var theForm = $("<form></form>").append(children);
    var success = function (data) {

        if (data.error) {
             current.html($(data.html).children());
            try {
                eval("load" + currentTab.capitalize() + "()");
            } catch (e) {
            
            }
            novosCamposLista(data.values_list);
            preencherCamposLista(data.values_list, data.errors_list);
        } else {
            current.append(children);
            try {
                eval("load" + currentTab.capitalize() + "()");
            } catch (e) {
            
            }
            $('.error-message', current).remove();
            $('.error', current).removeClass('error');
            currentTab = next[0].id;
            current.css("display", "none");
            next.css("display", "block");
            $("#botaoAnterior").css("display", "inline");
            if (currentTab == fim) {
                $("#botaoProximo").css("display", "none");
                $("#submitButton").css("display", "inline");
            }
        }
    }
    var options = {
        success: success,
        url: "/projetos/validar/",
        type: 'post',
        data: {'step_name': current[0].id},
        dataType:  'json'
        //target:        '#output1',   // target element(s) to be updated with server response
        //beforeSubmit:  showRequest,  // pre-submit callback
        //clearForm: true        // clear all form fields after successful submit
        //resetForm: true        // reset the form after successful submit
        // $.ajax options can be used here too, for example:
        //timeout:   3000
    };

    theForm.find("input[type=file]").each( function () {
        this.type = 'text';
    });
    theForm.ajaxSubmit(options);
}

function anterior() {
    var current = $("#"+currentTab);
    var previous = current.prev();
    current.css("display", "none");
    $("#submitButton").css("display", "none");
    currentTab = previous[0].id;
    previous.css("display", "block");
    $("#botaoProximo").css("display", "inline");
    if (currentTab == inicio) {
        $("#botaoAnterior").css("display", "none");
    }
}

////////////////////////////////////////////////////////////////////////////////

function loadRadioSingleExtra(o, v, id1, id2) {
    if ($(o).val()) {
        if ($(o).val () == v) {
            $('#' + id1).show();
            if (id2) {
                $('#' + id2).hide();
            }
        } else {
            $('#' + id1).hide();
            if (id2) {
                $('#' + id2).show();
            }
        }
    } else {
        $('#' + id1).hide();
        $('#' + id2).hide();
        
    }

}

function loadRadioMultipleExtra(o, v, id1, id2) {
    var li = $(o).parents("li")[0];
    if ($(o).val()) {
        if ($(o).val () == v) {
            $(li).addClass("subhead");
            $('#' + id1).show ();
            if (id2) {
                $('#' + id2).hide();
            }
        } else {
            $(li).removeClass("subhead");
            $('#' + id1).hide ();
            if (id2) {
                $('#' + id2).hide();
            }
        }
    } else {
        $(li).removeClass("subhead");
        $('#' + id1).hide();
        $('#' + id2).hide();
        
    }
}
