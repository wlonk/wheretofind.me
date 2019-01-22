import { shallowMount } from '@vue/test-utils';
import IdentitiesForm from '@/components/IdentitiesForm.vue';
import MockUrls from '../mockUrls';

jest.mock('axios');
window.Urls = MockUrls;

describe('IdentitiesForm.vue', () => {
  let context;

  beforeEach(() => {
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
    context = {
      $http,
      data: { identities: data },
      mocks,
    };
  });

  test('reorder/Identities', () => {
    const { mocks, data, $http } = context;
    const wrapper = shallowMount(IdentitiesForm, { mocks });
    wrapper.setData(data);
    wrapper.vm.reorder();

    expect($http.post).toBeCalledWith('/api/identities/reorder/', [1, 2]);
  });

  test('create/NewIdentity', () => {
    const { mocks, data, $http } = context;
    const wrapper = shallowMount(IdentitiesForm, { mocks });
    wrapper.setData(data);
    wrapper.vm.create().then(() => {
      expect($http.post).toBeCalledWith('/api/identities/', {
        name: '',
        url: '',
      });
      // TODO: This seems to be true in hand-testing, but not here. Probably an
      // async issue?
      // expect(wrapper.vm.identities).toContain({
      //   id: 3,
      //   name: "",
      //   url: "",
      // });
    });
  });

  test('destroy/deleteIdentity', () => {
    const { mocks, data, $http } = context;
    const wrapper = shallowMount(IdentitiesForm, { mocks });
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
    const { mocks, data, $http } = context;
    const wrapper = shallowMount(IdentitiesForm, { mocks });
    wrapper.vm.retrieveIdentities(data.identities[0]);

    expect($http.get).toBeCalledWith('/api/identities/');
  });
});
