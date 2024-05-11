def format_list_in_columns(strings, columns):
    import itertools
    
    # Dividir a lista em sub-listas de acordo com o número de colunas
    groups = [strings[i:i+columns] for i in range(0, len(strings), columns)]
    
    # Encontrar o comprimento máximo de cada coluna
    max_lengths = [max(len(item) for item in col) + 1 for col in itertools.zip_longest(*groups, fillvalue='')]
    
    # Criar uma string formatada
    result = "[/n"
    for group in groups:
        line = ' '.join(f"'{item}',".ljust(max_lengths[idx] + 2) for idx, item in enumerate(group))
        result += f"    {line}/n"
    result = result.rstrip('/n') + '/n]'
    
    return result