import numpy as np
from skimage.restoration._nl_means_denoising import _nl_means_denoising_2d, \
                    _nl_means_denoising_2drgb, _nl_means_denoising_3d, \
                    _fast_nl_means_denoising_2d, _fast_nl_means_denoising_3d, \
                    _fast_nl_means_denoising_2drgb

def nl_means_denoising(image, patch_size=7, patch_distance=11, h=0.1,
                       fast_mode=True):
    """
    Perform non-local means denoising on 2-D or 3-D grayscale images, and
    2-D RGB images.

    Parameters
    ----------
    image : ndarray
        input data to be denoised

    patch_size : int, optional
        size of patches used for denoising

    patch_distance : int, optional
        maximal distance in pixels where to search patches used for denoising

    h : float, optional
        cut-off distance (in gray levels). The higher h, the more permissive
        one is in accepting patches. A higher h results in a smoother image,
        at the expense of blurring features. For a Gaussian noise of standard
        deviation sigma, a rule of thumb is to choose the value of h to be
        sigma of slightly less.

    fast_mode : bool, optional
        if True (default value), a fast version of the non-local means
        algorithm is used. If False, the original version of non-local means is
        used. See the Notes section for more details about the algorithms.

    Returns
    -------

    result : ndarray
        denoised image, of same shape as `image`.

    See Also
    --------
    fast_nl_means_denoising

    Notes
    -----

    The non-local means algorithm is well suited for denoising images with
    specific textures. The principle of the algorithm is to average the value
    of a given pixel with values of other pixels in a limited neighbourhood,
    provided that the *patches* centered on the other pixels are similar enough
    to the patch centered on the pixel of interest.

    In the original version of the algorithm [1]_, corresponding to
    ``fast=False``, the computational complexity is

    image.size * patch_size ** image.ndim * patch_distance ** image.ndim

    Hence, changing the size of patches or their maximal distance has a
    strong effect on computing times, especially for 3-D images.

    However, the default behavior corresponds to ``fast=True``, for which
    another version of non-local means [2]_ is used, corresponding to a
    complexity of

    image.size * patch_distance ** image.ndim

    The computing time depends only weakly on the patch size, thanks to the
    computation of the integral of patches distances for a given shift, that
    reduces the number of operations [1]_. Therefore, this algorithm executes
    faster than `nl_means_denoising`, at the expense of using twice as much
    memory.

    Compared to the classic non-local means algorithm implemented in
    `nl_means_denoising`, all pixels of a patch contribute to the distance to
    another patch with the same weight, no matter their distance to the center
    of the patch. This coarser computation of the distance can result in a
    slightly poorer denoising performance. Moreover, for small images (images
    with a linear size that is only a few times the patch size), the classic
    algorithm can be faster due to boundary effects.

    The image is padded using the `reflect` mode of `skimage.util.pad`
    before denoising.

    References
    ----------
    .. [1] Buades, A., Coll, B., & Morel, J. M. (2005, June). A non-local
        algorithm for image denoising. In CVPR 2005, Vol. 2, pp. 60-65, IEEE.

    .. [2] Jacques Froment. Parameter-Free Fast Pixelwise Non-Local Means
           Denoising. Image Processing On Line, 2014, vol. 4, p. 300-326.

    Examples
    --------
    >>> a = np.zeros((40, 40))
    >>> a[10:-10, 10:-10] = 1.
    >>> a += 0.3*np.random.randn(*a.shape)
    >>> denoised_a = nl_means_denoising(a, 7, 5, 0.1)
    """
    if image.ndim == 2:
        if fast_mode:
            return np.array(_fast_nl_means_denoising_2d(image, s=patch_size,
                                            d=patch_distance, h=h))
        else:
            return np.array(_nl_means_denoising_2d(image, s=patch_size,
                                d=patch_distance, h=h))
    if image.ndim == 3 and image.shape[-1] > 4:  # only grayscale
        if fast_mode:
            return np.array(_fast_nl_means_denoising_3d(image, s=patch_size,
                                              d=patch_distance, h=h))
        else:
            return np.array(_nl_means_denoising_3d(image, patch_size,
                                patch_distance, h))
    if image.ndim == 3 and image.shape[-1] == 3:  # 2-D color (RGB) images
        if fast_mode:
            return np.array(_fast_nl_means_denoising_2drgb(image, patch_size,
                                patch_distance, h))
        else:
            return np.array(_nl_means_denoising_2drgb(image, patch_size,
                                patch_distance, h))
    else:
        raise ValueError("Non local means denoising is only possible for \
        2D grayscale and RGB images or 3-D grayscale images.")

