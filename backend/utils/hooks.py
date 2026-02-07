def capitalize_operation_hook(result, generator, request, public):
    # ECapitalize the first letter of the tag
    for path in result.get('paths', {}):
        for method in result['paths'][path]:
            tags = result['paths'][path][method].get('tags', [])
            result['paths'][path][method]['tags'] = [tag.capitalize() for tag in tags]
    return result
