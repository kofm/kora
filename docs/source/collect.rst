#########
 Collect
#########

The **Collect** application manages Plant Genetic Resources (PGR) reproductive material within your collection. It tracks samples, storage, inventory, and viability data, ensuring traceability and controlled stock management. The system supports the lifecycle of a sample.

*******
Samples
*******

Discarding a Sample
===================

To discard a sample:

1. Open the sample detail page.
2. Click **Delete**.
3. Confirm the action.

After a successful discard:

- The sample no longer appears in the main “Samples” list.
- The sample becomes visible in the “Discarded Samples” list.
- Its storage position is released and becomes available.
- The sample cannot be added to a cart.
- Historical data (weights, notes, variety, etc.) are preserved.
- The sample ID remains unavailable unless the sample is permanently deleted (reuse of sample IDs is discouraged).

Discarded samples are still considered during searches. If matches include discarded samples, you can access them by clicking the count of discarded matches displayed above the results table.

From the **Discarded Samples** listing, you can either restore or permanently delete samples.

Restoring a sample reactivates it and requires assigning a free storage position. The original position is not automatically reused. To restore a sample, click the green action button in the rightmost column of its row. The sample then returns to the active collection.

Permanent deletion is irreversible. Deletion removes the sample and all associated records (e.g. weight logs, germination data). To permanently delete a sample, click the red action button in the rightmost column of its row in the discarded samples listing. You can also bulk delete all matching discarded samples using the red link above the results table.

.. note::

   After permanent deletion, the sample and its associated records cannot be recovered.

*****
Carts
*****

Carts are containers for grouping samples to either withdraw material or discard samples from the active collection.

Two cart types are available:

- **Withdrawal carts** facilitate material withdrawal by reserving quantities and tracking deductions.
- **Discard carts** support controlled removal of obsolete or non-viable samples.

The **cart sidebar** is accessible via the tray icon beside the user menu in the top navigation bar.

.. _cart-sidebar:

Cart Sidebar
============

The selector at the top of the sidebar lets you choose the active cart. Each user can have one active cart at a time. The active cart is the target of all cart-related actions.

You can create, rename, clear, or delete a cart using the **cart menu**, accessible via the menu button next to the cart selector. From the same menu, you can download the cart’s content metadata in JSON format. Depending on the cart type, additional commands (e.g. **Withdraw** or **Discard**) are available.

You can add a sample to the active cart by:

- Clicking the tray action button in the rightmost column of the samples list.
- Clicking the tray action button in the rightmost column of the sample table on a variety detail page.
- Clicking **Add to cart** on a sample detail page.

A sample cannot be added twice to the same cart.

Withdrawal Carts
================

Withdrawal carts maintain a list of sample quantities to be retrieved. They may be used to locate material before retrieval or to export data (e.g. for label production).

Each withdrawal cart has a default withdrawal quantity applied to newly added samples. You can modify this default at any time.

When a sample is added:

- The specified quantity is reserved.
- The reserved amount is subtracted from the available quantity.
- The reservation appears in the :ref:`cart sidebar<cart-sidebar>`.

The total quantity and available quantity (total minus reservations) are visible in sample listings and on the sample detail page.

You can modify a reserved quantity while the cart is active by selecting the corresponding item in the sidebar. Removing an item from the cart releases its reservation.

To finalize retrieval, use the **Withdraw** command from the cart menu. This deducts the reserved quantities from the samples, updates weight logs, and completes the operation.

Discard Carts
=============

Discard carts remove samples from the active collection while preserving their data.

Unlike withdrawal carts:

- They do not manage quantities.
- They operate on whole samples.
- Their sidebar list is visually distinct from withdrawal carts.

After adding samples to a discard cart, use the **Discard** command from the cart menu to remove them from the active collection. Successfully discarded samples are removed from the cart.

.. note::

   A sample referenced by any active cart cannot be discarded.

Best Practices
==============

- Prefer discarding over permanent deletion unless removal is final.
- Finalize withdrawal carts promptly to ensure accurate availability.
- Review discard carts carefully before executing the discard command.
