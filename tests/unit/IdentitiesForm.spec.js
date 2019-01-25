import { shallowMount } from '@vue/test-utils';
import IdentitiesForm from '@/components/IdentitiesForm.vue';
import MockUrls from '../mockUrls';

jest.mock('axios');
window.Urls = MockUrls;

describe('IdentitiesForm.vue', () => {
  const setup = options => {
    const data = [
      {
        id: 1,
        name: 'Test 1',
        url: 'https://example.com/1',
      },
      {
        id: 2,
        name: 'Test 2',
        url: 'https://example.com/2',
      },
    ];
    const $http = {
      post: jest.fn().mockReturnValue(
        Promise.resolve({
          data: {
            id: 3,
            name: '',
            url: '',
          },
        }),
      ),
      get: jest.fn().mockResolvedValue({ data }),
      delete: jest.fn().mockResolvedValue(Promise.resolve()),
    };
    const mocks = {
      $http,
    };
    const mountOptions = {
      mocks,
      ...options,
    };
    const wrapper = shallowMount(IdentitiesForm, mountOptions);
    return {
      wrapper,
      $http,
      data: { identities: data },
      mocks,
    };
  };

  test('reorder/Identities', () => {
    const { wrapper, data, $http } = setup();
    wrapper.setData(data);
    wrapper.vm.reorder();

    expect($http.post).toBeCalledWith('/api/identities/reorder/', [1, 2]);
  });

  test('create/NewIdentity', () => {
    const { wrapper, data, $http } = setup();
    wrapper.setData(data);
    wrapper.vm
      .create()
      .then(() => {
        expect($http.post).toBeCalledWith('/api/identities/', {
          name: '',
          url: '',
        });
        return wrapper.vm.nextTick();
      })
      .then(() => {
        expect(wrapper.vm.identities).toContain({
          id: 3,
          name: '',
          url: '',
        });
      });
  });

  test('destroy/deleteIdentity', () => {
    const { wrapper, data, $http } = setup();
    wrapper.setData(data);
    wrapper.vm.destroy(data.identities[0]);

    expect($http.delete).toBeCalledWith('/api/identities/1/');
    expect(wrapper.vm.identities).not.toContain({
      id: 1,
      name: 'Test 1',
      url: 'https://example.com/1',
    });
  });

  test('retrieveIdentities', () => {
    const { wrapper, data, $http } = setup();
    wrapper.vm.retrieveIdentities(data.identities[0]);

    expect($http.get).toBeCalledWith('/api/identities/');
  });
});
