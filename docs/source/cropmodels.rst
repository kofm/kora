#############
 Crop Models
#############

The crop models framework allows you to define, register, and run models that compute outputs based on crop data and parameters. It is designed to be extensible and to integrate seamlessly with the overall *kora* system.

.. note::

   This feature is still in development and subject to changes.

Key features:

- **Model Definition:**  
  Each crop model is implemented as a subclass of the base `CropModel` class. Models declare required input parameters, optional inputs, and context information.

- **Inputs Declaration:**  
  Models specify which crop parameters they rely on via the `inputs` attribute. If any required parameter is missing for a particular crop, the model will not run.

- **Optional Inputs:**  
  Models can declare optional parameters that enhance functionality but are not strictly necessary to run.

- **Context and Naming:**  
  Models define a `context_name` for internal use and a human-readable `model_name` for display purposes.

- **Running Models:**  
  The main method to implement is `output()`, which performs computations using input parameters and properties such as crop area. Results should be stored in a dictionary under the `"value"` key and returned.

- **Execution Conditions:**  
  The `can_run()` method controls whether a model can execute, typically checking for parameter availability and any other relevant conditions like plot size.

- **Registration:**  
  After implementing a new model class (e.g., `MyModel`), it must be registered in the `init.py` file by adding it to the `AVAILABLE_CROP_MODELS` list. This ensures the model is available in the crop view and user interface.

- **Output Restrictions:**  
  Currently, only models producing a single numeric value as output are fully supported for downstream statistics.

Example usage snippet:

.. code-block:: python

   from calculator.modelling import CropModel

   class MyModel(CropModel):
       inputs = ["my_parameter"]
       inputs_optional = []
       context_name = "my_model"
       model_name = "My Model"

       def can_run(self):
           return super().can_run() & self.has_area()

       def output(self):
           context = super().output()
           result = self.get_parameter("my_parameter") * self.area.total_area
           context["value"] = result
           return context

Remember to register the model in `init.py`:

.. code-block:: python

   AVAILABLE_CROP_MODELS = [("mymodel", "MyModel")]
   STATISTICS_MODELS = [("mymodel", "MyModel")]

This modular approach allows you to easily add new crop models tailored to specific data and analysis needs.

.. note::

   The crop models system requires certain crop parameters to be present.
   If parameters are missing or plots lack area information, models will not run.
