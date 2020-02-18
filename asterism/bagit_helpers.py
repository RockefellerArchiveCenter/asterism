import bagit


def validate(bag_path):
    """Validates a bag against the BagIt specification"""
    bag = bagit.Bag(bag_path)
    return bag.validate()


def update_bag_info(bag_path, data):
    """Adds metadata from a dictionary to `bag-info.txt`"""
    assert(isinstance(data, dict))
    bag = bagit.Bag(bag_path)
    for k, v in data.items():
        bag.info[k] = v
    bag.save()


def update_manifests(bag_path):
    """Updates bag manifests according to BagIt specification"""
    bag = bagit.Bag(bag_path)
    bag.save(manifests=True)
