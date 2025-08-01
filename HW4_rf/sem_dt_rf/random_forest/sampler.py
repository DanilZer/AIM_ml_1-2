import numpy as np


class BaseSampler:
    def __init__(self, max_samples=1.0, bootstrap=False, random_state=None):
        """
        Parameters
        ----------
        bootstrap : Boolean
            if True then use bootstrap sampling
        max_samples : float in [0;1]
            proportion of sampled examples
        """
        self.random_state = np.random.RandomState(random_state)
        self.bootstrap = bootstrap
        self.max_samples = max_samples

    def sample_indices(self, n_features):
        """
        Parameters
        ----------
        n_features : int > 0
            initial number of features
        """
        n_selected_features = int(n_features * self.max_samples)

        if self.bootstrap:
            return self.random_state.randint(0, n_features, size=n_selected_features)
        else:
            return self.random_state.choice(n_features, size=n_selected_features, replace=False)

    def sample(self, x, y=None):
        # abstract method
        raise NotImplementedError


class ObjectSampler(BaseSampler):
    def __init__(self, max_samples=1.0, bootstrap=True, random_state=None):
        super().__init__(max_samples=max_samples, bootstrap=bootstrap, random_state=random_state)

    def sample(self, x, y=None):
        """
        Parameters
        ----------
        x : numpy ndarray of shape (n_objects, n_features)
        y : numpy ndarray of shape (n_objects,)

        Returns
        -------
        x_sampled, y_sampled : numpy ndarrays of shape (n_samples, n_features) and (n_samples,)
        """
        indices = super().sample_indices(x.shape[0])
        return x[indices], y[indices]

class FeatureSampler(BaseSampler):
    def __init__(self, max_samples=1.0, bootstrap=False, random_state=None): #не надо, в sclearn не так если оно True по умолчанию, то мы просто выкидываем фичи
        super().__init__(max_samples=max_samples, bootstrap=bootstrap, random_state=random_state)

    def sample(self, x, y=None):
        """
        Parameters
        ----------
        x : numpy ndarray of shape (n_objects, n_features)
        y : numpy ndarray of shape (n_objects,)

        Returns
        -------
        x_sampled : numpy ndarrays of shape (n_objects, n_features_sampled)
        """
        indices = super().sample_indices(x.shape[1])
        return x[:,indices]
