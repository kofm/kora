from describe.models import Protocol
from register.models import PlantVariety

# Get a variety
var = PlantVariety.objects.get(pk=1)

# Select a description
desc = var.description_set.first()

# Get the protocol
protocol = desc.protocol

# Get all the expressions in this description
expressions = desc.expression_set.all()

# Get all traits in the selected protocol
all_traits = protocol.trait_set.all()

# Print all traits within the selected protocol
exprs = []
for trait in all_traits:
    print(trait.description)
    expr = expressions.filter(state_of_expression__trait_id = trait.id)
    exprs.append(expr)


