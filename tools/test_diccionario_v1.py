import json
import os

def procesar_archivo(data):
    """Procesa la lista de datos y la convierte a JSON."""
    # Procesa los datos
    spawns = []
    blocks = []
    current_block = {}
    current_section = "spawns"  # Inicializar la sección actual

    for item in data:
        item = item.strip()  # Eliminar espacios en blanco al inicio y final
        if item.startswith('\t'):  # Bloques
            if current_section == "spawns":
                current_section = "blocks"  # Cambiar a la sección de bloques
                current_block = {}
            if 'rect' not in current_block:
                current_block['rect'] = list(map(int, item.split('\t')[1:]))
            elif 'enemies' not in current_block:
                current_block['enemies'] = list(map(int, item.split('\t')[1:]))
            elif 'clear' not in current_block:
                current_block['clear'] = list(map(int, item.split('\t')[1:]))
            elif 'text' not in current_block:
                current_block['text'] = item
                current_block['countdown'] = 0  # Agregar campo countdown
                blocks.append(current_block)
                current_block = {}
        else:  # Spawns
            if current_section == "spawns":
                if item.isdigit() or (item == '-1'):
                    spawns.append(int(item))
            else:
                # Si estamos en la sección de bloques, ignorar la línea
                pass 

    # Procesar blocks para añadir campos vacíos si no hay datos
    for block in blocks:
        if 'respawn' not in block:
            block['respawn'] = []
        if 'vip' not in block:
            block['vip'] = []
        if 'exceptional' not in block:
            block['exceptional'] = []

    # Crear el diccionario final
    result = {
        "spawns": spawns,
        "blocks": blocks
    }

    return result

# Datos del archivo .sac
data = ['127', '0\t430', '1\t431', '2\t-1', '3\t428', '4\t429', '5\t-1', '6\t-1', '7\t438', '8\t430', '9\t-1', '10\t430', '11\t-1', '12\t429', '13\t401', '14\t435', '15\t435', '16\t435', '17\t440', '18\t440', '19\t432', '20\t433', '21\t432', '22\t433', '23\t432', '24\t432', '25\t401', '26\t436', '27\t434', '28\t436', '29\t429', '30\t428', '31\t429', '32\t437', '33\t431', '34\t440', '35\t-1', '36\t428', '37\t429', '38\t440', '39\t-1', '40\t-1', '41\t430', '42\t438', '43\t82', '44\t83', '45\t84', '46\t83', '47\t401', '48\t435', '49\t435', '50\t435', '51\t440', '52\t440', '53\t-1', '54\t440', '55\t430', '56\t433', '57\t430', '58\t432', '59\t-1', '60\t432', '61\t433', '62\t432', '63\t401', '64\t434', '65\t436', '66\t436', '67\t434', '68\t439', '69\t439', '70\t439', '71\t401', '72\t443', '73\t443', '74\t443', '75\t443', '76\t428', '77\t429', '78\t-1', '79\t437', '80\t439', '81\t440', '82\t428', '83\t437', '84\t430', '85\t83', '86\t442', '87\t84', '88\t101', '89\t401', '90\t435', '91\t435', '92\t435', '93\t443', '94\t443', '95\t443', '96\t443', '97\t428', '98\t429', '99\t439', '100\t428', '101\t430', '102\t401', '103\t401', '104\t440', '105\t432', '106\t439', '107\t433', '108\t401', '109\t428', '110\t437', '111\t401', '112\t443', '113\t443', '114\t428', '115\t429', '116\t430', '117\t437', '118\t401', '119\t443', '120\t443', '121\t441', '122\t440', '123\t439', '124\t428', '125\t84', '126\t442', '', '11', '\t6\t\t37\t\t41\t\t25\t', '\t14\t\t0\t\t1\t\t2\t\t3\t\t4\t\t5\t\t6\t\t7\t\t8\t\t9\t\t10\t\t11\t\t12\t\t13\t', '\t0\t', '\t13\t\t0\t\t1\t\t2\t\t3\t\t4\t\t5\t\t6\t\t7\t\t8\t\t9\t\t10\t\t11\t\t12\t', '\t0\t', '\t0\t', '\t', '0\t', '\t43\t\t37\t\t58\t\t25\t', '\t12\t\t14\t\t15\t\t16\t\t17\t\t18\t\t19\t\t20\t\t21\t\t22\t\t23\t\t24\t\t25\t', '\t0\t', '\t8\t\t17\t\t18\t\t19\t\t20\t\t21\t\t22\t\t23\t\t24\t', '\t0\t', '\t0\t', '\t', '0\t', '\t60\t\t23\t\t91\t\t12\t', '\t22\t\t26\t\t27\t\t28\t\t29\t\t30\t\t31\t\t32\t\t33\t\t34\t\t35\t\t36\t\t37\t\t38\t\t39\t\t40\t\t41\t\t42\t\t43\t\t44\t\t45\t\t46\t\t47\t', '\t0\t', '\t14\t\t29\t\t30\t\t31\t\t32\t\t33\t\t34\t\t35\t\t36\t\t37\t\t38\t\t39\t\t40\t\t41\t\t42\t', '\t0\t', '\t4\t\t43\t\t44\t\t45\t\t46\t', '\t', '0\t', '\t95\t\t23\t\t108\t\t12\t', '\t16\t\t48\t\t49\t\t50\t\t51\t\t52\t\t53\t\t54\t\t55\t\t56\t\t57\t\t58\t\t59\t\t60\t\t61\t\t62\t\t63\t', '\t0\t', '\t12\t\t51\t\t52\t\t53\t\t54\t\t55\t\t56\t\t57\t\t58\t\t59\t\t60\t\t61\t\t62\t', '\t0\t', '\t0\t', '\t', '0\t', '\t105\t\t11\t\t116\t\t0\t', '\t8\t\t64\t\t65\t\t66\t\t67\t\t68\t\t69\t\t70\t\t71\t', '\t0\t', '\t3\t\t68\t\t69\t\t70\t', '\t0\t', '\t0\t', '\t', '0\t', '\t120\t\t11\t\t156\t\t0\t', '\t18\t\t72\t\t73\t\t74\t\t75\t\t76\t\t77\t\t78\t\t79\t\t80\t\t81\t\t82\t\t83\t\t84\t\t85\t\t86\t\t87\t\t88\t\t89\t', '\t0\t', '\t9\t\t76\t\t77\t\t78\t\t79\t\t80\t\t81\t\t82\t\t83\t\t84\t', '\t0\t', '\t4\t\t85\t\t86\t\t87\t\t88\t', '\t', '0\t', '\t158\t\t37\t\t176\t\t12\t', '\t14\t\t90\t\t91\t\t92\t\t93\t\t94\t\t95\t\t96\t\t97\t\t98\t\t99\t\t100\t\t101\t\t102\t\t103\t', '\t1\t\t101\t', '\t4\t\t97\t\t98\t\t99\t\t100\t', '\t0\t', '\t0\t', '\t', '0\t', '\t180\t\t11\t\t206\t\t0\t', '\t5\t\t104\t\t105\t\t106\t\t107\t\t108\t', '\t0\t', '\t2\t\t104\t\t106\t', '\t0\t', '\t0\t', '\t', '0\t', '\t158\t\t67\t\t176\t\t50\t', '\t3\t\t109\t\t110\t\t111\t', '\t1\t\t109\t', '\t1\t\t110\t', '\t0\t', '\t0\t', '\t', '0\t', '\t153\t\t84\t\t178\t\t70\t', '\t7\t\t112\t\t113\t\t114\t\t115\t\t116\t\t117\t\t118\t', '\t0\t', '\t4\t\t114\t\t115\t\t116\t\t117\t', '\t0\t', '\t2\t\t112\t\t113\t', '\t', '0\t', '\t153\t\t98\t\t178\t\t70\t', '\t8\t\t119\t\t120\t\t121\t\t122\t\t123\t\t124\t\t125\t\t126\t', '\t2\t\t122\t\t123\t', '\t1\t\t121\t', '\t1\t\t121\t', '\t2\t\t125\t\t126\t', '\t', '0\t']

# Procesa los datos y crea el JSON
result = procesar_archivo(data)
json_result = json.dumps(result, indent=4)  # Formato con sangría de 4 espacios

# Guarda el JSON en un archivo
with open("nuevo_archivo.json", 'w') as archivo_json:
    archivo_json.write(json_result)

print("Archivo JSON creado correctamente.")
