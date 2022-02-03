import SimpleITK as sitk
import os


def register(path_fixed_image, path_moving_image, output_folder, name_moving_image):
    fixed_image = sitk.ReadImage(path_fixed_image, sitk.sitkFloat32)
    moving_image = sitk.ReadImage(path_moving_image, sitk.sitkFloat32)
    output_dir = output_folder

    initial_transform = sitk.CenteredTransformInitializer(fixed_image,
                                                          moving_image,
                                                          sitk.Euler3DTransform(),
                                                          sitk.CenteredTransformInitializerFilter.MOMENTS)

    registration_method = sitk.ImageRegistrationMethod()

    # Similarity metric settings.
    registration_method.SetMetricAsMattesMutualInformation(numberOfHistogramBins=100)
    registration_method.SetMetricSamplingStrategy(registration_method.RANDOM)
    registration_method.SetMetricSamplingPercentage(0.01)

    registration_method.SetInterpolator(sitk.sitkLinear)

    # Optimizer settings.
    registration_method.SetOptimizerAsGradientDescent(learningRate=1.0, numberOfIterations=300, convergenceMinimumValue=1e-6, convergenceWindowSize=10)
    registration_method.SetOptimizerScalesFromPhysicalShift()

    # Setup for the multi-resolution framework.
    registration_method.SetShrinkFactorsPerLevel(shrinkFactors=[4, 2, 1])
    registration_method.SetSmoothingSigmasPerLevel(smoothingSigmas=[2, 1, 0])
    registration_method.SmoothingSigmasAreSpecifiedInPhysicalUnitsOn()

    # Set the initial moving and optimized transforms.
    optimized_transform = sitk.Euler3DTransform()
    registration_method.SetMovingInitialTransform(initial_transform)
    registration_method.SetInitialTransform(optimized_transform, inPlace=False)

    # Need to compose the transformations after registration.
    final_transform = sitk.CompositeTransform([registration_method.Execute(fixed_image, moving_image), initial_transform])

    # Always check the reason optimization terminated.
    print('Final metric value: {0}'.format(registration_method.GetMetricValue()))
    print('Optimizer\'s stopping condition, {0}'.format(registration_method.GetOptimizerStopConditionDescription()))

    moving_resampled = sitk.Resample(moving_image, moving_image, initial_transform, sitk.sitkLinear, 0.0, moving_image.GetPixelID())
    final_transform.FlattenTransform()

    sitk.WriteImage(moving_resampled, os.path.join(output_dir, name_moving_image + '_registered.nrrd'))
    # sitk.WriteTransform(final_transform, os.path.join(output_dir, name_moving_image + '_transform.tfm'))


def resampling(path_fixed_image, path_moving_image, output_folder, name_moving_image):
    fixed_image = sitk.ReadImage(path_fixed_image, sitk.sitkFloat32)
    moving_image = sitk.ReadImage(path_moving_image, sitk.sitkFloat32)
    output_dir = output_folder
    dimension = 3
    identity = sitk.Transform(dimension, sitk.sitkIdentity)
    moving_resampled = sitk.Resample(moving_image, fixed_image, identity, sitk.sitkNearestNeighbor, 0.0, moving_image.GetPixelID())
    sitk.WriteImage(moving_resampled, os.path.join(output_dir,  name_moving_image + '_resampled.nrrd'))
